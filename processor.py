#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unified Parking Data Merger
===========================

This script merges functionality from three scripts to create merged_parking_data.json:
- create_parking_registry.py: Create employee registry from Excel sheets
- merge_parking_data.py: Merge parking records with employee data
- parking_locations_manager.py: Manage and normalize parking locations

Usage:
    python unified_parking_merger.py <parking_records_excel> <parking_table_excel> [output_json]

Arguments:
    parking_records_excel - Excel file with parking records (e.g., parking_data.xlsx)
    parking_table_excel   - Excel file with employee data (e.g., Parking table.xlsx)
    output_json          - Output JSON file (optional, defaults to merged_parking_data.json)

Example:
    python unified_parking_merger.py parking_data.xlsx "Parking table.xlsx"
    python unified_parking_merger.py parking_data.xlsx "Parking table.xlsx" output.json

Output JSON Format:
{
  "cars": {
    "CB5347HX": {
      "name": "Христина Николова",
      "active_employee": true,
      "location": "А26 - МАЛЪК АНГЛИЙСКИ ДВОР"
    }
  },
  "records": [
    {
      "timestamp": 1761003937,
      "datetime": "2025-10-20 23:45:37",
      "direction": "exit",
      "plate": "CB5347HX"
    }
  ],
  "locations": {
    "print_shop": {
      "name": "Паркинг печатница",
      "spots": ["С36", "С37"]
    }
  }
}

Author: Unified merger combining create_parking_registry.py, merge_parking_data.py, parking_locations_manager.py
Date: 2025-11-05
"""

import pandas as pd
import json
import sys
import os
import re
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict


class UnifiedParkingMerger:
    """Unified parking data merger for Excel to JSON conversion."""

    def __init__(self, parking_records_file: str, parking_table_file: str, output_file: str = "parking_data.json"):
        self.parking_records_file = parking_records_file
        self.parking_table_file = parking_table_file
        self.output_file = output_file

        # Data storage
        self.parking_records = []
        self.cars_registry = {}
        self.parking_locations = {}

        # Statistics for reporting
        self.stats = {
            'total_records': 0,
            'unique_plates': 0,
            'registered_employees': 0,
            'unknown_plates': 0,
            'locations_count': 0
        }

    def normalize_plate(self, plate: str) -> str:
        """Normalize plate number by converting Cyrillic to Latin characters"""
        if pd.isna(plate) or not plate:
            return ""

        # Mapping of Cyrillic to Latin characters commonly used in Bulgarian plates
        cyrillic_to_latin = {
            'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O',
            'Р': 'P', 'С': 'C', 'Т': 'T', 'У': 'Y', 'Х': 'X', 'а': 'a', 'в': 'b',
            'е': 'e', 'к': 'k', 'м': 'm', 'н': 'h', 'о': 'o', 'р': 'p', 'с': 'c',
            'т': 't', 'у': 'y', 'х': 'x'
        }

        normalized = ""
        for char in str(plate):
            normalized += cyrillic_to_latin.get(char, char)

        return normalized.strip().upper()

    def split_registration_numbers(self, reg_str: str) -> List[str]:
        """Split registration numbers by / and clean them"""
        if pd.isna(reg_str) or str(reg_str).strip() == '':
            return []

        # Convert to string and split by /
        reg_numbers = str(reg_str).split('/')

        # Clean each registration number
        cleaned_numbers = []
        for reg in reg_numbers:
            cleaned = reg.strip()
            if cleaned and cleaned.lower() != 'nan':
                cleaned_numbers.append(cleaned)

        return cleaned_numbers

    def normalize_location_name(self, location: str) -> str:
        """Normalize location name to use Cyrillic А, В, С instead of Latin A, B, C"""
        if pd.isna(location) or not location:
            return ""

        # Convert Latin A, B, C to Cyrillic А, В, С in location
        normalized = str(location).replace('A', 'А').replace('B', 'В').replace('C', 'С')
        return normalized.strip()

    def extract_parking_spot(self, location: str) -> str:
        """Extract parking spot number from location string."""
        if pd.isna(location) or not location:
            return ""

        location_str = str(location).strip()

        # Look for patterns like "А23", "В134", "С37", etc.
        spot_match = re.search(r'([АВСDEFGHIJKLMNOPQRSTUVWXYZ]\d+)', location_str)
        if spot_match:
            return spot_match.group(1)

        return ""

    def determine_location_category(self, location: str) -> str:
        """Determine location category from location string."""
        if pd.isna(location) or not location:
            return "unknown"

        location_lower = str(location).lower()

        if 'подземен' in location_lower:
            return 'underground'
        elif 'покрит паркинг' in location_lower:
            return 'covered_parking'
        elif 'малък английски двор' in location_lower or 'малък англиски двор' in location_lower:
            return 'small_courtyard'
        elif 'голям английски двор' in location_lower or 'голям англиски двор' in location_lower:
            return 'large_courtyard'
        elif 'паркинг печатница' in location_lower:
            return 'print_shop'
        elif 'депо' in location_lower:
            return 'depot'
        elif 'зона' in location_lower:
            return 'zone'
        elif 'офис' in location_lower:
            return 'office_area'
        elif 'център' in location_lower:
            return 'center_area'
        elif 'външен' in location_lower:
            return 'external_area'
        else:
            return 'other'

    def get_location_display_name(self, category: str) -> str:
        """Get display name for location category."""
        display_names = {
            'underground': 'Подземен',
            'covered_parking': 'Покрит паркинг',
            'small_courtyard': 'Малък английски двор',
            'large_courtyard': 'Голям английски двор',
            'print_shop': 'Паркинг печатница',
            'depot': 'Депо',
            'zone': 'Зона',
            'office_area': 'Офис',
            'center_area': 'Център',
            'external_area': 'Външен'
        }
        return display_names.get(category, category.title())

    def create_parking_registry(self):
        """Create parking registry from Excel sheets (from create_parking_registry.py)"""
        print("👥 Creating parking registry from Excel sheets...")

        if not os.path.exists(self.parking_table_file):
            raise FileNotFoundError(f"Parking table file not found: {self.parking_table_file}")

        try:
            # Read both main sheets
            permanent_df = pd.read_excel(self.parking_table_file, sheet_name='Постоянни паркоместа')
            deleted_df = pd.read_excel(self.parking_table_file, sheet_name='Изтрити')

            print(f"   - Постоянни паркоместа: {len(permanent_df)} records")
            print(f"   - Изтрити: {len(deleted_df)} records")

            # Process permanent parking records
            processed_plates = set()
            for idx, row in permanent_df.iterrows():
                try:
                    reg_numbers = self.split_registration_numbers(row.iloc[0])  # First column: registration
                    employee_name = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else "Unknown"  # Second column: name
                    location = str(row.iloc[2]).strip() if not pd.isna(row.iloc[2]) else ""  # Third column: location

                    # Normalize location
                    normalized_location = self.normalize_location_name(location)

                    for reg_num in reg_numbers:
                        normalized_plate = self.normalize_plate(reg_num)
                        if normalized_plate:
                            self.cars_registry[normalized_plate] = {
                                'name': employee_name,
                                'active_employee': True,
                                'location': normalized_location
                            }
                            processed_plates.add(normalized_plate)

                            # Track parking locations
                            if normalized_location:
                                spot = self.extract_parking_spot(normalized_location)
                                category = self.determine_location_category(normalized_location)

                                if category not in self.parking_locations:
                                    self.parking_locations[category] = {
                                        'name': self.get_location_display_name(category),
                                        'spots': set()
                                    }

                                if spot:
                                    self.parking_locations[category]['spots'].add(spot)

                except Exception as e:
                    print(f"      ⚠️  Error processing permanent parking row {idx}: {e}")

            # Process Free column from permanent parking (column 4) to capture all parking spots
            print("   - Processing Free column locations...")
            free_locations_count = 0
            for idx, row in permanent_df.iterrows():
                try:
                    free_location = row.iloc[4] if len(row) > 4 else None
                    if not pd.isna(free_location) and str(free_location).strip():
                        normalized_location = self.normalize_location_name(free_location)
                        spot = self.extract_parking_spot(normalized_location)
                        category = self.determine_location_category(normalized_location)

                        if category not in self.parking_locations:
                            self.parking_locations[category] = {
                                'name': self.get_location_display_name(category),
                                'spots': set()
                            }

                        if spot:
                            self.parking_locations[category]['spots'].add(spot)
                            free_locations_count += 1

                except Exception as e:
                    print(f"      ⚠️  Error processing Free column row {idx}: {e}")

            print(f"   - Added {free_locations_count} locations from Free column")

            # Process deleted employees locations (from column 3)
            print("   - Processing Изтрити locations...")
            deleted_locations_count = 0
            for idx, row in deleted_df.iterrows():
                try:
                    reg_numbers = self.split_registration_numbers(row.iloc[0])  # First column: registration
                    employee_name = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else "Unknown"  # Second column: name

                    # Process location from Изтрити sheet (column 3)
                    location = ""
                    if len(row) > 3 and not pd.isna(row.iloc[3]):
                        location = str(row.iloc[3]).strip()
                        normalized_location = self.normalize_location_name(location)
                        spot = self.extract_parking_spot(normalized_location)
                        category = self.determine_location_category(normalized_location)

                        if category not in self.parking_locations:
                            self.parking_locations[category] = {
                                'name': self.get_location_display_name(category),
                                'spots': set()
                            }

                        if spot:
                            self.parking_locations[category]['spots'].add(spot)
                            deleted_locations_count += 1

                    for reg_num in reg_numbers:
                        normalized_plate = self.normalize_plate(reg_num)
                        if normalized_plate and normalized_plate not in processed_plates:
                            # Only add if not already in permanent parking
                            self.cars_registry[normalized_plate] = {
                                'name': employee_name,
                                'active_employee': False,
                                'location': ""
                            }

                except Exception as e:
                    print(f"      ⚠️  Error processing deleted employee row {idx}: {e}")

            print(f"   - Added {deleted_locations_count} locations from Изтрити sheet")
            print(f"✅ Parking registry created: {len(self.cars_registry)} entries")

        except Exception as e:
            raise Exception(f"Error creating parking registry: {e}")

    def load_parking_records(self):
        """Load parking data from Excel file (from merge_parking_data.py)"""
        print(f"📊 Loading parking records from: {self.parking_records_file}")

        if not os.path.exists(self.parking_records_file):
            raise FileNotFoundError(f"Parking records file not found: {self.parking_records_file}")

        try:
            # Find the header row by scanning for 'Време'
            df_scan = pd.read_excel(self.parking_records_file, header=None)
            header_row = None

            for i in range(min(50, len(df_scan))):
                row = df_scan.iloc[i]
                row_str = str(row.tolist())
                if 'Време' in row_str:
                    header_row = i
                    print(f"   - Found header at row {i}")
                    break

            if header_row is None:
                raise Exception("Could not find header row with 'Време' column")

            # Read with the correct header row
            df = pd.read_excel(self.parking_records_file, header=header_row)

            print(f"   - Found {len(df)} records")

            # Map column names
            column_mapping = {}
            for col in df.columns:
                col_lower = str(col).lower()
                if 'време' in col_lower:
                    column_mapping['datetime'] = col
                elif 'направление' in col_lower:
                    column_mapping['direction'] = col
                elif 'автомобил' in col_lower:
                    column_mapping['plate'] = col
                elif 'тип' in col_lower:
                    column_mapping['type'] = col

            # Process records
            valid_records = 0
            skipped_records = 0

            for idx, row in df.iterrows():
                try:
                    # Extract datetime
                    datetime_val = row[column_mapping.get('datetime', df.columns[0])]
                    if pd.isna(datetime_val):
                        skipped_records += 1
                        continue

                    # Parse Bulgarian datetime format: "20.10.2025 г. 23:45:37"
                    if isinstance(datetime_val, str):
                        try:
                            clean_datetime = datetime_val.replace(' г.', '')
                            dt = pd.to_datetime(clean_datetime, format='%d.%m.%Y %H:%M:%S')
                        except:
                            try:
                                dt = pd.to_datetime(datetime_val)
                            except:
                                skipped_records += 1
                                continue
                    else:
                        dt = datetime_val

                    # Extract direction
                    direction_val = row[column_mapping.get('direction', df.columns[1])]
                    if pd.isna(direction_val):
                        skipped_records += 1
                        continue

                    direction = str(direction_val).lower().strip()
                    plate = self.normalize_plate(row[column_mapping.get('plate', df.columns[2])])

                    if not plate:
                        skipped_records += 1
                        continue

                    # Map direction to English
                    if 'влизане' in direction or 'вход' in direction:
                        direction_en = 'enter'
                    elif 'излизане' in direction or 'изход' in direction:
                        direction_en = 'exit'
                    else:
                        direction_en = 'unknown'

                    # Create record
                    record = {
                        'timestamp': int(dt.timestamp()),
                        'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
                        'direction': direction_en,
                        'plate': plate
                    }

                    self.parking_records.append(record)
                    valid_records += 1

                except Exception as e:
                    skipped_records += 1
                    if skipped_records <= 5:  # Show only first 5 errors
                        print(f"   ⚠️  Skipping record {idx}: {e}")
                    continue

            self.stats['total_records'] = len(self.parking_records)
            unique_plates = set(record['plate'] for record in self.parking_records)
            self.stats['unique_plates'] = len(unique_plates)

            print(f"✅ Loaded {valid_records} valid parking records")
            print(f"   - Skipped {skipped_records} invalid records")
            print(f"   - Unique plates: {len(unique_plates)}")

        except Exception as e:
            raise Exception(f"Error loading parking records: {e}")

    def fix_missing_locations(self):
        """Check for cars with empty locations and look them up in Постоянни паркоместа"""
        print("🔍 Checking for missing locations in cars with active_employee: false...")
        print("   (searching in both Постоянни паркоместа and Изтрити sheets)")

        # Find cars with empty locations and active_employee: false
        cars_needing_locations = {}
        for plate, car_info in self.cars_registry.items():
            if (car_info.get('active_employee') == False and
                (car_info.get('location') == '' or car_info.get('location') is None)):
                cars_needing_locations[plate] = car_info

        if not cars_needing_locations:
            print("   - No cars with missing locations found")
            return

        print(f"   - Found {len(cars_needing_locations)} cars with missing locations")

        # Load both Постоянни паркоместа and Изтрити to search for these cars
        try:
            permanent_df = pd.read_excel(self.parking_table_file, sheet_name='Постоянни паркоместа')
            deleted_df = pd.read_excel(self.parking_table_file, sheet_name='Изтрити')

            # Create a lookup by employee name and plate
            name_to_location = {}

            # First check Постоянни паркоместа
            for idx, row in permanent_df.iterrows():
                try:
                    reg_numbers = self.split_registration_numbers(row.iloc[0])
                    employee_name = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else ""
                    location = str(row.iloc[2]).strip() if not pd.isna(row.iloc[2]) else ""

                    if employee_name and location:
                        normalized_location = self.normalize_location_name(location)
                        name_to_location[employee_name] = normalized_location

                        # Also map by registration number for direct lookup
                        for reg_num in reg_numbers:
                            normalized_plate = self.normalize_plate(reg_num)
                            if normalized_plate:
                                name_to_location[normalized_plate] = normalized_location

                except Exception as e:
                    continue

            # Then check Изтрити sheet for additional locations
            for idx, row in deleted_df.iterrows():
                try:
                    reg_numbers = self.split_registration_numbers(row.iloc[0])
                    employee_name = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else ""
                    # Check if Изтрити sheet has location column (usually column 3)
                    location = ""
                    if len(row) > 3 and not pd.isna(row.iloc[3]):
                        location = str(row.iloc[3]).strip()

                    if employee_name and location:
                        normalized_location = self.normalize_location_name(location)
                        # Only add if not already found in permanent parking
                        if employee_name not in name_to_location:
                            name_to_location[employee_name] = normalized_location

                        # Also map by registration number for direct lookup
                        for reg_num in reg_numbers:
                            normalized_plate = self.normalize_plate(reg_num)
                            if normalized_plate and normalized_plate not in name_to_location:
                                name_to_location[normalized_plate] = normalized_location

                except Exception as e:
                    continue

            # Try to find locations for cars with missing locations
            updated_count = 0
            for plate, car_info in cars_needing_locations.items():
                car_name = car_info.get('name', '')

                # Try to find location by name or plate
                found_location = None

                # First try by employee name
                if car_name in name_to_location:
                    found_location = name_to_location[car_name]

                # Then try by plate number
                elif plate in name_to_location:
                    found_location = name_to_location[plate]

                if found_location:
                    # Update the car's location but keep them as inactive employee
                    self.cars_registry[plate]['location'] = found_location
                    # Keep active_employee as False

                    print(f"   ✅ Updated {plate} ({car_name}): {found_location}")
                    updated_count += 1

                    # Add location to tracking if it's new
                    spot = self.extract_parking_spot(found_location)
                    category = self.determine_location_category(found_location)

                    if category not in self.parking_locations:
                        self.parking_locations[category] = {
                            'name': self.get_location_display_name(category),
                            'spots': set()
                        }

                    if spot:
                        self.parking_locations[category]['spots'].add(spot)

            print(f"   ✅ Updated {updated_count} cars with missing locations")

        except Exception as e:
            print(f"   ⚠️  Error looking up missing locations: {e}")

    def merge_and_finalize(self):
        """Merge data and finalize for output (from merge_parking_data.py + parking_locations_manager.py)"""
        print("🔄 Merging data and finalizing...")

        # Add any unknown plates from parking records to registry
        all_plates = set(record['plate'] for record in self.parking_records)

        for plate in all_plates:
            if plate not in self.cars_registry:
                self.cars_registry[plate] = {
                    'name': 'Unknown',
                    'active_employee': False,
                    'location': ""
                }

        # Fix missing locations for cars with active_employee: false
        self.fix_missing_locations()

        # Normalize parking locations (from parking_locations_manager.py)
        # Convert sets to sorted lists
        for category, info in self.parking_locations.items():
            if isinstance(info['spots'], set):
                info['spots'] = sorted(list(info['spots']))

        # Update statistics
        self.stats['registered_employees'] = len([c for c in self.cars_registry.values() if c.get('active_employee', False)])
        self.stats['unknown_plates'] = len([c for c in self.cars_registry.values() if c.get('name') == 'Unknown'])
        self.stats['locations_count'] = len(self.parking_locations)

        print(f"✅ Merge complete")
        print(f"   - Total cars: {len(self.cars_registry)}")
        print(f"   - Active employees: {self.stats['registered_employees']}")
        print(f"   - Unknown plates: {self.stats['unknown_plates']}")
        print(f"   - Location categories: {self.stats['locations_count']}")

    def create_output_json(self):
        """Create the final JSON output in the exact format required"""
        print("📄 Creating JSON output...")

        # Create the exact JSON structure as specified
        output_data = {
            'cars': self.cars_registry,
            'records': sorted(self.parking_records, key=lambda x: x['timestamp']),
            'locations': self.parking_locations
        }

        # Save to file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"✅ JSON output saved to: {self.output_file}")
        print(f"   - File size: {os.path.getsize(self.output_file) / 1024:.1f} KB")

        return output_data

    def run(self):
        """Run the complete unified merge process"""
        print("🚀 Starting Unified Parking Data Merger")
        print("=" * 50)
        print("Merging functionality from:")
        print("  - create_parking_registry.py")
        print("  - merge_parking_data.py")
        print("  - parking_locations_manager.py")
        print("=" * 50)

        try:
            # Step 1: Create parking registry from Excel sheets
            self.create_parking_registry()

            # Step 2: Load parking data records
            self.load_parking_records()

            # Step 3: Merge data and finalize
            self.merge_and_finalize()

            # Step 4: Create final JSON
            result = self.create_output_json()

            print("\n🎉 Unified merge completed successfully!")
            print("=" * 50)
            print(f"📊 Final Statistics:")
            print(f"   - Total parking records: {self.stats['total_records']:,}")
            print(f"   - Unique vehicles: {self.stats['unique_plates']:,}")
            print(f"   - Active employees: {self.stats['registered_employees']:,}")
            print(f"   - Unknown plates: {self.stats['unknown_plates']:,}")
            print(f"   - Parking locations: {self.stats['locations_count']:,}")
            print(f"📁 Output file: {self.output_file}")

            return result

        except Exception as e:
            print(f"\n❌ Error during unified merge process: {e}")
            raise


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 3:
        print("Unified Parking Data Merger")
        print("=" * 35)
        print("Usage: python unified_parking_merger.py <parking_records_excel> <parking_table_excel> [output_json]")
        print("\nArguments:")
        print("  parking_records_excel - Excel file with parking records (e.g., parking_data.xlsx)")
        print("  parking_table_excel   - Excel file with employee data (e.g., 'Parking table.xlsx')")
        print("  output_json          - Output JSON file (optional, defaults to merged_parking_data.json)")
        print("\nExample:")
        print("  python unified_parking_merger.py parking_data.xlsx 'Parking table.xlsx'")
        print("  python unified_parking_merger.py parking_data.xlsx 'Parking table.xlsx' output.json")
        print("\nThis script merges functionality from:")
        print("  - create_parking_registry.py")
        print("  - merge_parking_data.py")
        print("  - parking_locations_manager.py")
        print("\nOutput JSON Format:")
        print('  {')
        print('    "cars": {"CB5347HX": {"name": "Христина Николова", "active_employee": true, "location": "А26 - МАЛЪК АНГЛИЙСКИ ДВОР"}},')
        print('    "records": [{"timestamp": 1761003937, "datetime": "2025-10-20 23:45:37", "direction": "exit", "plate": "CB5347HX"}],')
        print('    "locations": {"print_shop": {"name": "Паркинг печатница", "spots": ["С36", "С37"]}}')
        print('  }')
        return

    parking_records_file = sys.argv[1]
    parking_table_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "parking_data.json"

    # Create and run unified merger
    merger = UnifiedParkingMerger(parking_records_file, parking_table_file, output_file)
    merger.run()


if __name__ == "__main__":
    main()
import os
import csv
from datetime import date
from difflib import SequenceMatcher

DATA_FILE = "campus_items.txt"
FIELDS = ["id", "type", "name", "category", "description",
          "location", "date", "contact", "status"]


def load_items():
    """Read reports from a normal text file."""
    items = []

    if not os.path.exists(DATA_FILE):
        return items

    try:
        with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="|")
            for row in reader:
                row["id"] = int(row["id"])
                items.append(row)
    except (OSError, ValueError, KeyError):
        print("Warning: The data file could not be read.")

    return items


def save_items(items):
    """Write all reports to a normal text file."""
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, delimiter="|")
        writer.writeheader()
        writer.writerows(items)


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def similarity(text1, text2):
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def show_matches(items, lost_item):
    matches = []

    for item in items:
        if item["type"] == "FOUND" and item["status"] == "OPEN":
            category_score = similarity(lost_item["category"], item["category"])
            name_score = similarity(lost_item["name"], item["name"])
            description_score = similarity(lost_item["description"], item["description"])
            location_score = similarity(lost_item["location"], item["location"])

            score = (
                0.35 * category_score
                + 0.30 * name_score
                + 0.25 * description_score
                + 0.10 * location_score
            )

            if score >= 0.35:
                matches.append((score, item))

    matches.sort(key=lambda result: result[0], reverse=True)

    print("\n--- Possible Matches ---")
    if not matches:
        print("No possible match found yet. Check again later.")
        return

    for score, item in matches[:5]:
        print(f"\nMatch score: {score * 100:.1f}%")
        print(f"Report ID: #{item['id']}")
        print(f"Item: {item['name']} | Category: {item['category']}")
        print(f"Description: {item['description']}")
        print(f"Location: {item['location']} | Date: {item['date']}")
        print(f"Contact: {item['contact']}")

    print("\nThese are only suggestions. Verify ownership before returning an item.")


def add_report(items, report_type):
    print(f"\n--- Report a {report_type.title()} Item ---")

    new_id = max((item["id"] for item in items), default=0) + 1

    new_item = {
        "id": new_id,
        "type": report_type,
        "name": get_text("Item name: "),
        "category": get_text("Category (ID card/books/electronics/etc.): "),
        "description": get_text("Description (colour, brand, marks, etc.): "),
        "location": get_text("Where was it lost/found? "),
        "date": input(f"Date (YYYY-MM-DD, Enter for {date.today()}): ").strip()
                or str(date.today()),
        "contact": get_text("Contact detail: "),
        "status": "OPEN"
    }

    items.append(new_item)
    save_items(items)
    print(f"\nReport saved successfully. Your report ID is #{new_id}.")

    if report_type == "LOST":
        show_matches(items, new_item)


def view_reports(items):
    print("\n--- All Campus Reports ---")
    if not items:
        print("No reports available.")
        return

    for item in items:
        print(f"\nID: #{item['id']} | Type: {item['type']} | Status: {item['status']}")
        print(f"Item: {item['name']} | Category: {item['category']}")
        print(f"Description: {item['description']}")
        print(f"Location: {item['location']} | Date: {item['date']}")
        print(f"Contact: {item['contact']}")


def search_reports(items):
    keyword = get_text("\nEnter a keyword (item/category/description/location): ").lower()
    found = []

    for item in items:
        searchable_text = (
            item["name"] + " " + item["category"] + " " +
            item["description"] + " " + item["location"]
        ).lower()

        if keyword in searchable_text and item["status"] == "OPEN":
            found.append(item)

    print("\n--- Search Results ---")
    if not found:
        print("No matching open reports found.")
    else:
        view_reports(found)


def find_matches_by_id(items):
    try:
        lost_id = int(input("\nEnter the LOST report ID: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for item in items:
        if item["id"] == lost_id and item["type"] == "LOST":
            show_matches(items, item)
            return

    print("No LOST report found with that ID.")


def mark_returned(items):
    try:
        item_id = int(input("\nEnter the report ID to mark as returned: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for item in items:
        if item["id"] == item_id:
            if item["status"] == "RETURNED":
                print("This report is already marked as returned.")
                return

            confirm = input(f"Mark '{item['name']}' as returned? (y/n): ").lower()
            if confirm == "y":
                item["status"] = "RETURNED"
                save_items(items)
                print("Report updated successfully.")
            else:
                print("No changes made.")
            return

    print("No report exists with that ID.")


def main():
    items = load_items()

    print("=" * 50)
    print("       CAMPUSFIND - SMART LOST & FOUND")
    print("=" * 50)

    while True:
        print("""
1. Report a LOST item
2. Report a FOUND item
3. View all reports
4. Search open reports
5. Find possible matches for a lost report
6. Mark an item as returned
7. Exit
""")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_report(items, "LOST")
        elif choice == "2":
            add_report(items, "FOUND")
        elif choice == "3":
            view_reports(items)
        elif choice == "4":
            search_reports(items)
        elif choice == "5":
            find_matches_by_id(items)
        elif choice == "6":
            mark_returned(items)
        elif choice == "7":
            print("Thank you for using CampusFind. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()

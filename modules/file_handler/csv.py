import os, csv


def saveCSV(activity_name, deeplink, package_name, csv_dir):
    os.makedirs(csv_dir, exist_ok=True)
    csv_file = os.path.join(csv_dir, f"{package_name}.csv")
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([activity_name, deeplink])

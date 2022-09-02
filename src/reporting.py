from prettytable import PrettyTable

def output_report(r):
    artist_album_heading = ["Track", "Rating"]
    generic_heading = ["Artist", "Album", "Year", "Rating"]

    report_type = r[0]
    report = r[1]

    if report_type == "artist_album": 
        print(report[0][0] + " - " + report[0][1] + " (" + str(report[0][2]) + ")")
        output_table = PrettyTable(artist_album_heading)
        for row in report:
            output_table.add_row([row[4], row[5]])
    else:
        output_table = PrettyTable(generic_heading)
        output_table.add_rows(report)

    print(output_table)
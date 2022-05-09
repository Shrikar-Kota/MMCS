import os

def save_summary_to_file(summary, OUTPUT_PATH, fileid, emailhash):
    with open(os.path.join(OUTPUT_PATH, f"{emailhash}_{fileid}.txt"), "w") as f:
        list_summary = summary.split(".")
        paragraphs = []; current_paragraph = ""; linenumber = 0
        while linenumber < len(list_summary):
            linecount = 0
            while linecount < 5 and linenumber < len(list_summary):
                current_paragraph += list_summary[linenumber]
                linecount += 1
                linenumber += 1
            paragraphs.append(current_paragraph)
            
        f.writelines(paragraphs)
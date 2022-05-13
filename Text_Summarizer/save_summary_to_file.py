import os

def save_summary_to_file(summary, OUTPUT_PATH, fileid, emailhash):
    with open(os.path.join(OUTPUT_PATH, f"{emailhash}_{fileid}.txt"), "w", errors='ignore') as f:
        list_summary = summary.split(".")
        paragraphs = []; linenumber = 0
        while linenumber < len(list_summary):
            linecount = 0; current_paragraph = []
            while linecount < 5 and linenumber < len(list_summary):
                current_paragraph.append(list_summary[linenumber])
                linecount += 1
                linenumber += 1
            paragraphs.append(".".join(current_paragraph))
            
        f.writelines(paragraphs)
from pypdf import PdfWriter

def merge_pdfs():
   merger = PdfWriter()
   merger.append("dec.pdf")
   merger.append("assignment9.pdf")
   merger.write("week10assignment.pdf")
   merger.close()
   print("merged!")

if __name__ == "__main__":
  merge_pdfs()
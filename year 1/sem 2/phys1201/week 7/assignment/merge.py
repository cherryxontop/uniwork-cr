from pypdf import PdfWriter

def merge_pdfs():
   merger = PdfWriter()
   merger.append("dec.pdf")
   merger.append("assignment6.pdf")
   merger.write("assignment6sub.pdf")
   merger.close()
   print("merged!")

if __name__ == "__main__":
  merge_pdfs()
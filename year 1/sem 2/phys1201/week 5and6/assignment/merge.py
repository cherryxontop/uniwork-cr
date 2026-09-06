from pypdf import PdfWriter

def merge_pdfs():
   merger = PdfWriter()
   merger.append("dec.pdf")
   merger.append("physassignment5.pdf")
   merger.write("assignment5sub.pdf")
   merger.close()
   print("merged!")

if __name__ == "__main__":
  merge_pdfs()
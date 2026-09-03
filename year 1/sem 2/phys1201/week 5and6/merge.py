from pypdf import PdfWriter

def merge_pdfs():
   merger = PdfWriter()
   merger.append("integdec.pdf")
   merger.append("lab.pdf")
   merger.write("labfinal.pdf")
   merger.close()
   print("merged!")

if __name__ == "__main__":
  merge_pdfs()
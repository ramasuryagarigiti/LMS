# import mysql.connector as ms
#
# def ex():
#
#     try:
#         mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@")
#         cu = mydb.cursor()
#         cu.execute("use grp");cu.execute("select books.book from books where yr=3")
#         lst=cu.fetchall();
#
#         def bintofile(bindata, filename):
#             with open(pdf, bindata) as file:
#                 file.write(bindata)
#         rname="C:\\Users\\shanm\\OneDrive\\Desktop\\Pycharm.pdf"
#         for i in lst:
#
#         with open(i[8], rname) as file:
#             file.write(bindata,rname)
#
#
#         cu.close()
#     except Exception as e:
#         print("Error is:-",e)
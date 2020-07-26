import sqlite3
import datetime
import pytz
import ast
import requests

x = datetime.datetime.now(pytz.timezone('Asia/Yerevan'))

conn = sqlite3.connect("db/post.db")
c = conn.cursor()

conn1 = sqlite3.connect("db/user.db")
c1 = conn1.cursor()


while True:
	for i in c.execute("SELECT * FROM posts").fetchall():
		x = datetime.datetime.now(pytz.timezone('Asia/Yerevan'))

		try:

			if int(i[3].split(" ")[1].split(":")[1]) <  int(x.strftime("%M")):
				#print(i[0])
				if int(i[3].split(" ")[1].split(":")[0]) <= int(x.strftime("%H")):
					if int(i[3].split(" ")[0].split("-")[0]) <= int(x.strftime("%d")):
						if int(i[3].split(" ")[0].split("-")[1]) <= int(x.strftime("%m")):
							if int(i[3].split(" ")[0].split("-")[2]) <= int(x.strftime("%Y")):
								print("DELETEED POST  " + str(i[0]))
								user_notef_unr = ast.literal_eval(c1.execute("SELECT * FROM " + str(i[11])).fetchall()[0][9].strip())[0]
								user_notef_r = ast.literal_eval(c1.execute("SELECT * FROM " + str(i[11])).fetchall()[0][9].strip())[1]
								print(user_notef_unr)
								print(user_notef_r)
								user_new_unr = []
								user_new_r = []
								for k in user_notef_r:
									if len(k.split("||||")) > 2:
										if int(k.split("||||")[1]) == int(i[0]):
											print("DELETEED THAT UNREAD POST")
										else:
											user_new_r.append(k)
									else:
										user_new_r.append(k)

								for j in user_notef_unr:
									if len(j.split("||||")) > 2:
										if int(j.split("||||")[1]) == int(i[0]):
											print("DELETEED THAT READ POST")
										else:
											user_new_unr.append(j)
									else:
										user_new_unr.append(j)

								notef_str = str([user_new_unr, user_new_r])
								print(notef_str)
								c1.execute("UPDATE " + str(i[11]) + " SET note = '" + notef_str.replace("'", '"') + "'")
								c.execute("DELETE FROM posts WHERE id='" + str(i[0]) + "'")
								conn1.commit()
								conn.commit()
								r = requests.get("https://codetg.cf/tarber_out")

		except:
			pass

	conn.commit()
	conn1.commit()
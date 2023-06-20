import sqlite3

from PyQt5.QtWidgets import QMessageBox

from consts import themes, mnths


class storage_db:
    def __init__(self):
        self.app = None
        self.con = sqlite3.connect("expense.db")
        self.conn_cur = self.con.cursor()

    def create_tables(self):
        self.conn_cur.execute(
            """CREATE TABLE IF NOT EXISTS expenses (Id INT, Category TEXT, Spend INT, SpendDate TEXT, InsertDate TEXT)""")
        self.conn_cur.execute(
            """CREATE TABLE IF NOT EXISTS categories (Category TEXT, Description TEXT)""")
        self.conn_cur.execute(
            """CREATE TABLE IF NOT EXISTS incomes (Income INT, Source TEXT, SpendDate TEXT)""")
        self.conn_cur.execute(
            """CREATE TABLE IF NOT EXISTS themes (Theme TEXT UNIQUE)""")
        self.conn_cur.execute(
            """CREATE TABLE IF NOT EXISTS profile (username TEXT NOT NULL, password TEXT NOT NULL)""")
        self.con.close()

    def get_data_for_main(self, month, year):
        data = self.conn_cur.execute("""SELECT * FROM expenses WHERE strftime('%m', SpendDate) = ?
            AND strftime('%Y', SpendDate) = ? ORDER BY Id ASC""", (mnths.months[month], year))
        data = data.fetchall()
        self.con.close()

        return data

    def get_data_main(self):
        data = self.conn_cur.execute(
            """SELECT * FROM expenses ORDER BY Id ASC""")
        data = data.fetchall()
        self.con.close()

        return data

    def delete_expense(self, del_id):
        self.conn_cur.execute("DELETE FROM expenses WHERE Id = ?", (del_id,))
        self.con.commit()
        self.con.close()

    def get_ctgs(self):
        ctgs = self.conn_cur.execute("SELECT Category from categories")
        ctgs = ctgs.fetchall()
        self.con.close()

        return ctgs

    def check_exist_ctg(self, ctg_name, ctg_des):
        ctgs = self.conn_cur.execute(
            "SELECT Category from categories WHERE Category = ?", (ctg_name,))
        ctgs = ctgs.fetchone()

        return ctgs

    def insert_ctg(self,  ctg_name, ctg_des):
        self.conn_cur.execute(f"""INSERT INTO categories (Category, Description)
                        VALUES (?,?)""", (ctg_name, ctg_des,))
        self.con.commit()
        self.con.close()

    def check_exist_exp(self, Id):
        id = self.conn_cur.execute("SELECT Id from expenses WHERE Id=?", (Id,))
        ids = id.fetchone()

        return ids

    def insert_exp(self, Id, ctg, spend, spenddate):
        self.conn_cur.execute(f"""INSERT INTO expenses (Id, Category, Spend, SpendDate, InsertDate)
                    VALUES (?,?,?,?, DATE('now'))""", (Id, ctg, spend, spenddate.toString("yyyy-MM-dd")))
        self.con.commit()
        self.con.close()

    def apply_theme(self, app):
        self.app = app
        self.conn_cur.execute("""SELECT Theme FROM themes""")
        theme = self.conn_cur.fetchone()
        if theme is None or theme[0] == "Light":
            self.app.setStyleSheet(None)
        else:
            self.app.setStyleSheet(themes.theme_dark)
        self.con.close()

    def apply_settings(self, text):
        self.conn_cur.execute("DELETE FROM themes")
        self.conn_cur.execute("INSERT INTO themes (Theme) VALUES (?)", (text,))
        self.con.commit()
        self.con.close()

    def get_income(self, month, year):
        inc = self.conn_cur.execute("SELECT SUM(Income) from incomes")
        incs = inc.fetchone()

        cur_inc = self.conn_cur.execute("""SELECT SUM(Income) from incomes WHERE strftime('%m', SpendDate) = ? 
                    AND strftime('%Y', SpendDate) = ?""", (mnths.months[month], str(year)))
        cur_incs = cur_inc.fetchone()

        self.con.close()

        return incs, cur_incs

    def insert_income(self, add_inc, source, income_date):
        self.conn_cur.execute(f"""INSERT INTO incomes (Income, Source, SpendDate)
                VALUES (?,?,?)""", (add_inc, source, income_date.toString("yyyy-MM-dd")))
        self.con.commit()
        self.con.close()

    def upd_exp(self, spend, spenddate, Id):
        self.conn_cur.execute(f"UPDATE expenses SET Spend = ?, SpendDate = ? WHERE Id = ?",
                              (spend, spenddate.toString("yyyy-MM-dd"), Id,))
        self.con.commit()
        self.con.close()

    def get_exp_info(self, Id):
        items = self.conn_cur.execute(
            "SELECT * from expenses WHERE Id = ?", (Id,))
        items = items.fetchall()
        self.con.close()

        return items

    def get_years_for_smry(self):
        yrss = []
        years_exp = self.conn_cur.execute(
            "SELECT DISTINCT strftime('%Y', SpendDate) FROM expenses ORDER BY SpendDate ASC")
        yrs_exp = years_exp.fetchall()

        years_inc = self.conn_cur.execute(
            "SELECT DISTINCT strftime('%Y', SpendDate) FROM incomes ORDER BY SpendDate ASC")
        yrs_inc = years_inc.fetchall()
        self.con.close()

        for yr in yrs_inc:
            yrss.append(yr[0])

        for year in yrs_exp:
            if year[0] not in yrss:
                yrss.append(year[0])
        yrss.sort()

        return yrss

    def get_data_for_smry(self, month, year):
        spent = 0
        income = 0

        year = str(year)

        total_spent = self.conn_cur.execute("""SELECT SUM(Spend) FROM expenses WHERE strftime('%m', SpendDate) = ? AND 
            strftime('%Y', SpendDate) = ?""", (mnths.months[month], year,))
        total_spent = total_spent.fetchall()

        total_income = self.conn_cur.execute("""SELECT SUM(Income) from incomes WHERE strftime('%m', SpendDate) = ? 
            AND strftime('%Y', SpendDate) = ?""", (mnths.months[month], year))
        incs = total_income.fetchall()

        spend = self.conn_cur.execute("""SELECT Category, SUM(Spend) AS total_spent from expenses WHERE strftime('%m', SpendDate) = ?
            AND strftime('%Y', SpendDate) = ? GROUP BY Category""", (mnths.months[month], year))
        spend = spend.fetchall()
        self.con.close()

        for y in total_spent:
            if y[0] is not None:
                spent = y[0]
            else:
                spent = "00"

        for x in incs:
            if x[0] is not None:
                income = x[0]
            else:
                income = "00"

        rem_income = int(income) - int(spent)

        return spent, income, rem_income, spend

    def create_profile(self, username, password):
        self.conn_cur.execute('''CREATE TRIGGER IF NOT EXISTS enforce_single_row
                            BEFORE INSERT ON profile
                            BEGIN
                                SELECT CASE
                                    WHEN (SELECT COUNT(*) FROM profile) >= 1
                                    THEN RAISE(ABORT, 'Table already has a row')
                                END;
                            END;''')
        try:
            self.conn_cur.execute(
                "INSERT INTO profile (username, password) VALUES (?, ?)", (username, password))
        except sqlite3.Error:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("User Exists")
            msgBox.setText("There can only be one user at a time")
            msgBox.setStyleSheet("""QPushButton {
                    min-width: 100px;
                    min-height: 30px;
                    max-width: 100px;
                    max-height: 30px;
                }""")
            msgBox.exec_()
        self.con.commit()
        self.con.close()

    def get_user_info(self, username, password):
        user_info = self.conn_cur.execute(
            "SELECT * FROM profile WHERE username=? AND password=?", (username, password))
        user = user_info.fetchone()

        self.con.close()

        return user

    def reset_data(self):
        self.conn_cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.conn_cur.fetchall()
        for table in tables:
            table_name = table[0]
            if table_name != "profile":
                self.conn_cur.execute(f"DELETE FROM {table_name}")

        self.con.commit()
        self.con.close()

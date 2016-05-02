import sqlite3
import sys, os

class DbAccess:
    
    def __init__(self):
        self.db_file = 'db.sqlite3'
        self.con = None
        self.connect()
    
    def connect(self):
        try:
            self.con = sqlite3.connect(self.db_file)
        except sqlite3.Error, e:
            print 'connect() Error %s:' % e.args[0]
            self.close()
            sys.exit(1)
    
    def close(self):
        if self.con:
            self.con.close()
            
    def test(self):
        try:
            cursor = self.con.cursor()    
            cursor.execute('SELECT SQLITE_VERSION()')
            data = cursor.fetchone()
            print 'SQLite version: %s' % data                
        except sqlite3.Error, e:
            print 'test() Error %s:' % e.args[0]
            self.close()
            sys.exit(1)
    
    def entry_get_id(self, entry_date):
        try:
            cursor = self.con.cursor()    
            params = (entry_date,)
            
            cursor.execute('''
                SELECT id 
                FROM viewer_entry 
                WHERE date = ?'''
                , params)
                            
            data = cursor.fetchone()
        except sqlite3.Error, e:
            print 'entry_get_id() Error %s:' % e.args[0]
            self.close()
            sys.exit(1)
        return data
        
    def exchangerate_get_id(self, entry_id, currency):
        try:
            cursor = self.con.cursor()    
            params = (entry_id, currency)
            cursor.execute('''
                SELECT id 
                FROM viewer_exchangerate 
                WHERE entry_id = ? AND currency = ?'''
                , params)
                            
            data = cursor.fetchone()
        except sqlite3.Error, e:
            print 'exchangerate_get_id() Error %s:' % e.args[0]
            self.close()
            sys.exit(1)
        return data
    
    def insert_exchangeRate(self, entry_id, currency, rate):
        if self.exchangerate_get_id(entry_id, currency) == None:
            try:
                print 'Inserting %s - %s...' % (currency, rate)
                cursor = self.con.cursor()
                params = (currency, rate, entry_id,)
                cursor.execute('''
                    INSERT INTO viewer_exchangerate(currency, rate, entry_id) 
                    VALUES (?, ?, ?)'''
                    , params)
                                
                self.con.commit()
            except sqlite3.Error, e:
                print 'insert_exchangeRate() insert Error %s:' % e.args[0]
                self.close()
                sys.exit(1)
        else:
            try:
                print 'Updating %s - %s...' % (currency, rate)
                cursor = self.con.cursor()
                params = (rate, entry_id, currency,)
                cursor.execute('''
                    UPDATE viewer_exchangerate 
                    SET rate = ? 
                    WHERE entry_id = ? AND currency = ?'''
                    , params)
                                
                self.con.commit()
            except sqlite3.Error, e:
                print 'insert_exchangeRate() update Error %s:' % e.args[0]
                self.close()
                sys.exit(1)
                
        return cursor.lastrowid
        
    def insert_entry(self, entry_date):
        if self.entry_get_id(entry_date) == None:
            try:
                cursor = self.con.cursor()    
                params = (entry_date,)
                cursor.execute('''
                    INSERT INTO viewer_entry(date) 
                    VALUES (?)'''
                    , params)
                                
                self.con.commit()
                
                return cursor.lastrowid
            except sqlite3.Error, e:
                print 'insert_entry() Error %s:' % e.args[0]
                self.close()
                sys.exit(1)
        else:
            return -1
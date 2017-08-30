#!/usr/bin/env python

import sqlite3

class Auth:
    def __init__(self, db='quipper', testing=False):
        """Auth library"""
        self.db = db
        self.users_table = 'users'
        self.privileges_table = 'privileges'
        if testing:
            self.users_table += '_test'
            self.privileges_table += '_test'

    def needadmin(self, f):
        def decor(s, bot, update):
            room = update.message.chat_id
            user = update.message.from_user.id
            if self.get_user_privilege(user, room) != 'admin':
                bot.sendMessage(room, text="You don't have this privilege")
                return 
            return f(s, bot, update)
        return decor

    def get_user_privilege(self, user, room):
        """ Check if a user has privileges in a room """
        db = self.users_table
        if user == 296246016:
            return 'admin'
        try:
            with sqlite3.connect('quipper') as conn:
                c = conn.cursor()
                c.execute("select id,room,role,username from {}".format(db))
                users = c.fetchall()
                # Room
                # -Role
                # --User
                user_list = {}
                for id, room, role, u in users:
                    if str(id) == str(user):
                        return role
                return 'user'
        except Exception as e:
            return "I failed to check user privileges\n{}".format(repr(e))

from utils.db_service import MySQLConnector

class UsersController(object):
    """
    'users controller' for controlling 'flights' table from aircompany database
    """

    def __init__(self):
        """
        initialize new 'users' controller
        """
        MySQLConnector().connect()
        self.cursor = MySQLConnector.INSTANCE.get_cursor()

    def create(self,id, email, password, name, phone, address, last_name, city, state, postal_code, country, id_role):
        """
        create new row in 'users' table with info:
        :param email: user's email
        :param password: user's password
        :param name: user's name
        :param phone: user's phone
        :param address: user's address
        :param last_name: user's last_name
        :param city: user's city
        :param state: user's state
        :param postal_code: user's postal_code
        :param country: user's country
        :param id_role: user's id_role
        :return: responce from mysql databases
        """

        MySQLConnector.INSTANCE.execute_query('use aircompany;')
        MySQLConnector.INSTANCE.execute_query('INSERT INTO users(email, password, name, phone, address, last_name, city,'
                                              ' state, postal_code, country, id_role) values ({0},{1},{2},{3},{4},{5},'
                                              '{6},{7},{8},{9},{10});'.format(email, password, name, phone,
                                                        address, last_name, city,state, postal_code, country, id_role))

    def read(self):
        """
        select info from 'users' table
        :return: selected info
        """
        MySQLConnector.INSTANCE.execute_query('SELECT * FROM users;')
        return MySQLConnector.INSTANCE.get_results()

    def read_by_id(self, id):
        """
        select info from 'users' table
        :id: user's id
        :return: selected info
        """
        MySQLConnector.INSTANCE.execute_query('SELECT * FROM users WHERE id = {0};'.format(id))
        return MySQLConnector.INSTANCE.get_results()

    def update(self, email, phone, id):
        """
        update 'users' table with info
        """
        MySQLConnector.INSTANCE.execute_query('UPDATE users SET email = {0}, phone = {1} WHERE id = {2};'
                                              .format(email, phone, id))

    def delete(self, id):
        """
        delete info from 'users' table, info:

        :return: mysql database responce
        """
        MySQLConnector.INSTANCE.execute_query('DELETE FROM users WHERE id = {0}'.format(id))
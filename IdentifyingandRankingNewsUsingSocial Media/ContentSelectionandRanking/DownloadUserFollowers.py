import xlrd
import twint
import xlsxwriter


def get_users_handles():
    user_handles = list()
    wb = xlrd.open_workbook(r'C:\Users\Esraa\Desktop\MainProcessesIdea\Tweets\tweetsdata.xlsx')
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        handle = sheet.cell_value(i, 4)
        if str(handle).__contains__('@'):
            user_handles.append(str(handle)[1:])
        else:
            user_handles.append(str(handle))
    return user_handles


def get_followers(username):
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    try:
        twint.run.Followers(c)
        list_of_followers = twint.storage.panda.Follow_df
    except():
        print("get_followers method exception")
        return list()

    return list_of_followers['followers'][username]


def get_followers_of_users():
    followings = {}
    user_handles = get_users_handles()
    workbook = xlsxwriter.Workbook('Exception.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for handle in user_handles:
        if handle == 'handle':
            continue
        print("New handle " + str(handle))
        try:
            followings[handle] = get_followers(handle)
        except KeyError:
            worksheet.write(row, 0, handle)
            row += 1
    workbook.close()
    workbook = xlsxwriter.Workbook('users_followers.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    print("saved in followers file")
    for user, followers in followings.items():
        for follower in followers:
            worksheet.write(row, 0, user)
            worksheet.write(row, 1, follower)
            row += 1
    workbook.close()


get_followers_of_users()

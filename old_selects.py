from create_db import Database
from parse_data import Parser
import os
from datetime import date, time, datetime, timedelta
import pprint
import plotly
import plotly.graph_objs as go

pp = pprint.PrettyPrinter(indent=2)
db = Database("sensor_data.db")

wtf = "2015-10-26T11:40:34.0000000Z"

# Get maximum of values by unit


def get_max_all():
    query = "SELECT MAX(VALUE) as MAX, UNIT FROM sensor GROUP BY UNIT"
    max_all = db.select_values(query)
    pp.pprint(max_all)

# Get minimum of values by unit


def get_min_all():
    query = "SELECT MIN(VALUE) as MIN, UNIT FROM sensor GROUP BY UNIT"
    min_all = db.select_values(query)
    pp.pprint(min_all)

# Get number of rows by unit


def get_count_all():
    query = "SELECT COUNT(*) as COUNT, UNIT FROM sensor GROUP BY UNIT"
    count_all = db.select_values(query)
    pp.pprint(count_all)

# Sum of all values by unit


def get_sum_all():
    query = "SELECT SUM(VALUE) as SUM_OF_UNIT_VALUES, UNIT FROM sensor GROUP BY UNIT"
    sum_all = db.select_values(query)
    pp.pprint(sum_all)

# Average of the values by unit


def get_avg_all():
    query = "SELECT AVG(VALUE) as AVG_OF_VALUES, UNIT FROM sensor GROUP BY UNIT"
    avg_all = db.select_values(query)
    pp.pprint(avg_all)


def weekly_select():
    last_date_query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
    last_date = db.select_values(last_date_query)

    # print("2015-12-09T18:02:44.000000Z")
    # print(last_date[0][0])
    # print(last_date[0])
    # print(type(last_date))
    # weekly_query = "SELECT * FROM sensor WHERE TIME BETWEEN DATETIME(" + str(
    # last_date[0][0]) + ", '-7 days') AND \"" + str(last_date[0][0]) + "\""
    weekly_query = "SELECT * FROM sensor WHERE TIME >= DATETIME(\"" + \
        last_date[0][0] + "\", '-7 days') AND TIME <= DATETIME(\"" + \
        last_date[0][0] + "\")"
    # print(weekly_query)
    weekly = db.select_values(weekly_query)

    pp.pprint(weekly)


def monthly_select():
    query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
    last_date = db.select_values(query)

    monthly_query = "SELECT * FROM sensor WHERE TIME >= DATETIME(\"" + \
        last_date[0][0] + "\", 'start of month') AND TIME <= DATETIME(\"" +\
        last_date[0][0] + "\")"

    monthly = db.select_values(monthly_query)

    # pp.pprint(monthly)
    return monthly


def yearly_select():
    query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
    last_date = db.select_values(query)

    yearly_query = "SELECT * FROM sensor WHERE TIME >= DATETIME(\"" + \
        last_date[0][0] + "\", 'start of year') AND TIME <= DATETIME(\"" +\
        last_date[0][0] + "\")"

    yearly = db.select_values(yearly_query)

    # pp.pprint(yearly)
    return yearly


def daily_select():
    query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
    last_date = db.select_values(query)

    daily_query = "SELECT * FROM sensor WHERE TIME >= DATETIME(\"" + \
        last_date[0][0] + "\", '-1 day') AND TIME <= DATETIME(\"" +\
        last_date[0][0] + "\")"

    daily = db.select_values(daily_query)

    # pp.pprint(daily)
    return daily


# Here we create the 2 lists that are going to be plotly's arguments
# daily
daily_plot_x = []
daily_plot_y = []
daily_plot = daily_select()
for daily in range(len(daily_plot)):
    daily_plot_x.append(daily_plot[daily][2])

for daily in range(len(daily_plot)):
    daily_plot_y.append(int(daily_plot[daily][1]))

daily_datetime = []
for i in range(len(daily_plot_x)):
    daily_datetime.append(datetime.strptime(daily_plot_x[i], "%Y-%m-%dT%H:%M:%S.%fZ"))


# Here we create the 2 lists that are going to be plotly's arguments
# monthly
monthly_plot_x = []
monthly_plot_y = []
monthly_plot = monthly_select()
for monthly in range(len(monthly_plot)):
    monthly_plot_x.append(monthly_plot[monthly][2])

for monthly in range(len(monthly_plot)):
    monthly_plot_y.append(int(monthly_plot[monthly][1]))

test_datetime = []
for i in range(len(monthly_plot_x)):
    test_datetime.append(datetime.strptime(monthly_plot_x[i], "%Y-%m-%dT%H:%M:%S.%fZ"))

# pp.pprint(monthly_plot_y)

# yearly
yearly_plot_x = []
yearly_plot_y = []
yearly_plot = yearly_select()
for yearly in range(len(yearly_plot)):
    yearly_plot_x.append(yearly_plot[yearly][2])

for yearly in range(len(yearly_plot)):
    yearly_plot_y.append(int(yearly_plot[yearly][1]))

yearly_datetime = []
for i in range(len(yearly_plot_x)):
    yearly_datetime.append(datetime.strptime(yearly_plot_x[i], "%Y-%m-%dT%H:%M:%S.%fZ"))

# pp.pprint(yearly_plot_y)
# Create a new list with monthly X axis converted in datetime objects

# ---------------------------------------------------------------------------------
# d = timedelta(days=1)
# trace1 = go.Scatter(
#     x=daily_datetime,
#     y=daily_plot_y,
#     mode='markers')
# data = [trace1]
# layout = go.Layout(xaxis=dict(
#                    range=[daily_datetime[0]-d,
#                           daily_datetime[-1]+d]
#                    ))
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='daily.html', auto_open=True)
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# d = timedelta(days=1)
# trace1 = go.Scatter(
#     x=test_datetime,
#     y=monthly_plot_y,
#     mode='markers')
# data = [trace1]
# layout = go.Layout(xaxis=dict(
#                    range=[test_datetime[0]-d,
#                           test_datetime[-1]+d]
#                    ),
#                    title="Alpine_K81_Height",
#                    autosize=True,
#                    annotations=[
#     dict(
#         x=0.5,
#         y=-0.09,
#         showarrow=False,
#         text="nope",
#         xref='paper',
#         yref='paper'
#     ),
#     dict(
#         x=-0.04,
#         y=0.5,
#         showarrow=False,
#         text='Custom y-axis title',
#         textangle=-90,
#         xref='paper',
#         yref='paper'
#     )
# ]
# )
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='monthly.html', auto_open=True)
# ---------------------------------------------------------------------------------
d = timedelta(days=1)
trace1 = go.Scatter(
    x=yearly_datetime,
    y=yearly_plot_y,
    mode='markers')
data = [trace1]
layout = go.Layout(xaxis=dict(
    range=[yearly_datetime[0]-d,
           yearly_datetime[-1]+d]
))
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='yearly.html', auto_open=True)
# ---------------------------------------------------------------------------------
# d = timedelta(days=1)
# trace1 = go.Bar(
#     x=yearly_datetime,
#     y=yearly_plot_y)
# # mode='markers')
# data = [trace1]
# layout = go.Layout(xaxis=dict(
#                    range=[yearly_datetime[0]-d,
#                           yearly_datetime[-1]+d]),
#
#                    bargap=0.15,
#                    bargroupgap=0
#                    )
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='yearly.html', auto_open=True)
# ---------------------------------------------------------------------------------


# ---- PLOT DATA USING PLOTLY (works but got issues with how it shows the bars) -----

# Store in plot_data the Bar Graphic Object
# plot_data=[go.Bar(x=test_datetime, y=monthly_plot_y)]

# Plot the Bar Graphic Object
# plotly.offline.plot(fig, filename='yearly.html', auto_open=True)

# print(type(monthly_plot_y[0]))

# -----------------------------------------------------------------------------------


# get_max_all()
# get_min_all()
# get_count_all()
# get_sum_all()
# get_avg_all()
# weekly_select()
# "SELECT TIME, CASE WHEN DATETIME(%s, '-7 days') \
#      == DATETIME(%s) THEN 'TRUE' END FROM sensor" % (last_date, wtf)

# """SELECT CASE
#  WHEN DATEDIFF(week, %s, TIME) == 1 THEN 'TRUE'
#  ELSE 'FALSE'
#  END
# , *
# FROM sensor""" % last_date
#

# last_date_query = """SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"""
# last_date = db.select_values(last_date_query)
# print(last_date)

# lista = db.select_all()
# # pp.pprint(lista)
#
# weekly = []
# for dates in range(len(lista)):
#     if datetime.strptime(lista[dates][-1], "%Y-%m-%dT%H:%M:%S.0%fZ") < \
#             datetime.strptime(lista[-1][-1], "%Y-%m-%dT%H:%M:%S.0%fZ"):
#         weekly.append(lista[dates][-1])
#     # dummy = datetime.strptime(lista[date][-1], "%Y-%m-%dT%H:%M:%S.0%fZ")
#
#     # print(lista[dates][-1])
# print(weekly)
#
# """SELECT *
# FROM sensor
# WHERE TIME BETWEEN DATETIME("2015-12-09T18:02:44.000000Z", '-7 days')\
# AND DATETIME ("2015-12-09T18:02:44.000000Z") """
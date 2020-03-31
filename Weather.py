import json
import requests
import discord
import datetime

# from PIL import Image, ImageDraw, ImageFont
import os
# import plotly.graph_objects as go
from discord.ext import commands

class Weather(commands.Cog):
	@commands.command(pass_context=True)
	async def weather(self, ctx):
		if ctx.channel.id == int(567179438047887381):
			conditions = json.loads(requests.get("https://api.weather.com/v2/turbo/vt1hourlyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode=42.27%2C-71.80&language=en-US&units=e").text)
			observations = json.loads(requests.get("https://api.weather.com/v2/turbo/vt1observation?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode=42.27%2C-71.80&language=en-US&units=e").text)

			# Current
			temperature = observations["vt1observation"]["temperature"]
			feelsLike = observations["vt1observation"]["feelsLike"]
			windSpeed = observations["vt1observation"]["windSpeed"]
			windDirection = observations["vt1observation"]["windDirCompass"]
			precipChance = observations["vt1observation"]["precip24Hour"]
			phrase = observations["vt1observation"]["phrase"]

			# Get precipitation and temperature throughout the day?

			await ctx.send(str(phrase) + "\nTemperature: " + str(temperature) + " °F\nFeels Like: " + str(feelsLike) + " °F\nWind Speed: " + str(windSpeed) + " mph " + windDirection)

	# Forecast
	@commands.command(pass_context=True)
	async def forecast(self, ctx):
		"""
		Sends the weather forecast for tomorrow
		"""
		if ctx.channel.id == int(567179438047887381):
			forecast = json.loads(requests.get("https://api.weather.com/v2/turbo/vt1dailyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode=42.27%2C-71.80&language=en-US&units=e").text)

			dayOfWeek = forecast["vt1dailyForecast"]["dayOfWeek"][1]
			temperature = forecast["vt1dailyForecast"]["day"]["temperature"][1]
			precipChance = forecast["vt1dailyForecast"]["day"]["precipPct"][1]
			phrase = forecast["vt1dailyForecast"]["day"]["phrase"][1]
			await ctx.send(str(dayOfWeek) + "\n" + str(phrase) + "\nTemperature: " + str(temperature) + " °F\nPrecipitation Chance: " + str(precipChance) + "%")

	# @commands.command(pass_context=True)
	# async def test(self, ctx):
	# 	now = datetime.datetime.now()
	#
	# 	times = []
	# 	for i in range(0, 11):
	# 		times.append(str(now.hour) + ":00")
	# 		now = now + datetime.timedelta(hours=1)
	#
	# 	observations = json.loads(requests.get(
	# 		"https://api.weather.com/v2/turbo/vt1observation?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode=42.27%2C-71.80&language=en-US&units=e").text)
	# 	conditions = json.loads(requests.get(
	# 		"https://api.weather.com/v2/turbo/vt1hourlyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode=42.27%2C-71.80&language=en-US&units=e").text)
	#
	# 	temperature = observations["vt1observation"]["temperature"]
	# 	feelsLike = observations["vt1observation"]["feelsLike"]
	# 	windSpeed = observations["vt1observation"]["windSpeed"]
	# 	windDirection = observations["vt1observation"]["windDirCompass"]
	# 	precipChance = observations["vt1observation"]["precip24Hour"]
	# 	phrase = observations["vt1observation"]["phrase"]
	#
	# 	nextTwelve = conditions["vt1hourlyForecast"]["temperature"][0:11]
	#
	# 	fig = go.Figure()
	# 	fig.add_trace(go.Scatter(x=times, y=nextTwelve, mode="lines+markers+text", name='Temperatures',
	# 							 line=dict(color='royalblue', width=4), text=nextTwelve, textfont_size=20,
	# 							 textposition="top center"))
	#
	# 	# fig.update_layout(title='Temperatures over the next 12 hours', xaxis_title='Time', yaxis_title='Temperature (°F)')
	#
	# 	fig.update_layout(
	# 		xaxis=dict(
	# 			type="category",
	# 			showline=True,
	# 			showgrid=False,
	# 			showticklabels=True,
	# 			linecolor='rgb(204, 204, 204)',
	# 			linewidth=2,
	# 			ticks='outside',
	# 			tickfont=dict(
	# 				family='Arial',
	# 				size=17,
	# 				color='rgb(82, 82, 82)',
	# 			),
	# 		),
	# 		yaxis=dict(
	# 			showgrid=False,
	# 			zeroline=False,
	# 			showline=False,
	# 			showticklabels=False,
	# 		),
	# 		autosize=False,
	# 		margin=dict(
	# 			autoexpand=False,
	# 			l=0,
	# 			r=0,
	# 			t=0,
	# 			b=30,
	# 		),
	# 		showlegend=False,
	# 		plot_bgcolor='white'
	# 	)
	#
	# 	fig.update_yaxes(automargin=True, range=[min(nextTwelve) - 1, max(nextTwelve) + 2])
	#
	# 	fig.write_image(format="png", width=800, height=400, file=os.path.join("assets", "weather", "temp", "graph.png"))
	#
	# 	background = Image.open(os.path.join("assets", "weather", "Background.png"))
	# 	graph = Image.open(os.path.join("assets", "weather", "temp", "graph.png"))
	# 	weatherLogo = Image.open(os.path.join("assets", "weather", "Test.png"))
	#
	# 	background.paste(graph, (0, 400, 800, 800), graph)
	#
	# 	text = ImageDraw.Draw(background)
	# 	font = ImageFont.truetype("arial.ttf", 60)
	# 	text.text((20, 10), phrase, fill=(0, 0, 0), font=font)
	#
	# 	font = ImageFont.truetype("arial.ttf", 70)
	# 	text.text((300, 190), str(temperature) + " °F", fill=(0, 0, 0), font=font)
	#
	# 	text.text((600, 100), str(windDirection), fill=(0, 0, 0), font=font)
	# 	text.text((550, 190), str(windSpeed) + " mph", fill=(0, 0, 0), font=font)
	#
	# 	background.paste(weatherLogo, (20, 100, 270, 350))
	#
	# 	background.save(os.path.join("assets", "weather", "temp", "fig1.png"))
	#
	# 	await ctx.send(file=discord.File(os.path.join("assets", "weather", "temp", "fig1.png")))
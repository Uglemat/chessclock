time_in_seconds = 10 * 60
startside = "left"
resolution = (800, 600)
fontsize = 150
fullscreen = False
textcolor = {
    "right": "white",
    "left":  (30, 30, 30)
}
active_textcolor = "red" # The text color for the active player
bgcolor = {
    "right": (30, 30, 30),
    "left":  "white"
}

def timeformat(millisecs):
    """
    Used to format the time left for the players before displaying it
    """
    return "{}:{:0>2}".format(*divmod(int(millisecs/1000), 60))

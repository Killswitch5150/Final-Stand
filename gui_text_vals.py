import game_fonts

#dependencies
button_color_dark = (100, 100, 100) #define dark button color
button_color_light = (254, 254, 0) #define light button color
button1_color_dark = (100, 100, 100)
button1_color_light = (254, 254, 0)

#only enter static values (no f strings or vars) the game will not be able to read them
game_over_text = game_fonts.font.render(f"Game Over.", True, (255, 0, 0)) 
restart_text = game_fonts.font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
text = game_fonts.smallfont.render('PLAY', True, button_color_light) #create label for play button
text2 = game_fonts.smallfont.render('CONTROLS', True, button_color_light) #create label for controls button
varControls = "Game Controls:"
varGClineone = "Up/Down Arrow Keys or 'W' and 'S' keys to move"
varGClinetwo = "'R' to reload"
varGClinethree = "Spacebar to shoot"
varGClinefour = "Ammo drops randomly spawn to give you more ammo"
title_text1 = game_fonts.font2.render(varControls, True, (255, 0, 0))
title_text2 = game_fonts.con_font2.render(varGClineone, True, (255, 0, 0))
title_text3 = game_fonts.con_font2.render(varGClinetwo, True, (255, 0, 0))
title_text4 = game_fonts.con_font2.render(varGClinethree, True, (255, 0, 0))
title_text5 = game_fonts.con_font2.render(varGClinefour, True, (255, 0, 0))
backtext = game_fonts.smallfont.render('BACK', True, button1_color_light) #create object for back button text
        
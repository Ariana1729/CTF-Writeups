import random

good_image = """
				TUX's KITCHEN
                    ..- - .              
                   '        `.           
                  '.- .  .--. .          
                 |: _ | :  _ :|          
                 |`(@)--`.(@) |          
                 : .'     `-, :          
                 :(_____.-'.' `          
                 : `-.__.-'   :          
                 `  _.    _.   .         
                /  /  `_ '  \\    .       
               .  :          \\   \\      
              .  : _      __  .\\   .     
             .  /             : `.  \\    
            :  /      '        : `.  .   
           '  `      :          : :  `.  
         .`_ :       :          / '   |  
         :' \\ .      :           '__  :  
      .--'   \\`-._    .      .' :    `).  
    ..|       \\   )          :   '._.'  : 
   ;           \\-'.        ..:         / 
   '.           \\  - ....-   |        '  
      -.         :   _____   |      .'   
        ` -.    .'--       --`.   .'     
            `--                --    
"""

flag = open('flag.txt','r').read()
MY_LUCKY_NUMBER = 29486316

# I need to bake special stuff!
def bake_it():
	s = 0
	for i in range(random.randint(10000,99999)):
		s = random.randint(100000000000,999999999999)
	s -= random.randint(232,24895235)
	return random.randint(100000000000,999999999999)

# Create my random mess
def rand0m_mess(food,key):
	mess = []
	mess.append(key)
	art = key
	bart = bake_it()
	cart = bake_it()
	dart = bake_it()
	for i in range(len(food)-1):
		art = (art*bart+cart)%dart
		mess.append(art)
	return mess

# Gotta prepare the food!!!
def prepare(food):
	good_food = []
	for i in range(len(food)):
		good_food.append(food[i]^MY_LUCKY_NUMBER)
	for k in range(len(good_food)):
		good_food[i] += MY_LUCKY_NUMBER
	return good_food

# Bake it!!!
def final_baking(food,key):
	baked = rand0m_mess(food,key)
	treasure = []
	for i in range(len(baked)):
		treasure.append(ord(food[i])*baked[i])
	treasure = prepare(treasure)
	return treasure

print(good_image)
key = bake_it()
print(final_baking(flag,key))

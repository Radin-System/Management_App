CONSOLE_WELCOME:str = r'''
/'\_/`\                                                            ( )_ 
|     |   _ _   ___     _ _    __     __    ___ ___     __    ___  | ,_)
| (_) | /'_` )/' _ `\ /'_` ) /'_ `\ /'__`\/' _ ` _ `\ /'__`\/' _ `\| |  
| | | |( (_| || ( ) |( (_| |( (_) |(  ___/| ( ) ( ) |(  ___/| ( ) || |_ 
(_) (_)`\__,_)(_) (_)`\__,_)`\__  |`\____)(_) (_) (_)`\____)(_) (_)`\__)
                            ( )_) |                                     
                             \___/'                                     
                       _____  ___    ___                                
                      (  _  )(  _`\ (  _`\                              
    ______  ______    | (_) || |_) )| |_) )    ______  ______           
   (______)(______)   |  _  || ,__/'| ,__/'   (______)(______)          
                      | | | || |    | |                                 
                      (_) (_)(_)    (_)                                 
                                                                        
- Welcome to the application console
- For get commands detail type:
    > help
'''

CONSOLE_HELP:str = '''
- Commands:
  > help
      Shows help

  > status
      Shows the status of Components

  > components
      prints the componnets in dict format

  > processes
      prints the processes list in dict format

  > reassign_dependencies
      Refreshes the Dependencies of all components

  > start <Componnet Name>
      starts the mentiond componnet

  > stop <Componnet Name>
      stops the mentiond componnet

  > start_all
      Starts all of the componnets

  > stop_all
      Stops all of the componnets

  > exit or Control-C
      Exits the console
'''
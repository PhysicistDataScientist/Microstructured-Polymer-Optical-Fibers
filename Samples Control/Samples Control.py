# Comments:
'''
None.
'''

# Libraries:
from random import randint
from os.path import exists, join
from datetime import datetime, timedelta
from pandas import read_excel, to_datetime, ExcelWriter, isnull
from matplotlib.pyplot import subplots, show

# Classes:

# Functions:
## Introduction to the program:
def intro():
    print('-----------------------------')
    print('Welcome to "Samples Control"!')
    print('-----------------------------')
    print('With this program you will be able to:')
    print('1. Keep counts of the samples on each drying chamber;')
    print('2. Decide the actions to be taken for each sample;')
    print('3. Visualize these actions;')
    print('4. Modify the control sheet.')
    print()
    print('Let\'s start!')
    print()
## Find the path to the sample files: 
def get_folder():
    global folder
    while True:
        with open("Samples Path Manager.txt", mode='rt') as f:
            folder = f.read()
            f.close()
        try: 
            if not exists(folder):
                raise FileExistsError('There is no folder with such path!')
            else:
                break
        except FileExistsError as fee:
            print(fee)
            print('Go to the "Samples Path Manager.txt" and change its content!')
            print()
            input('Type anything when you are done: ')
## Pre configuration:
def pre_config(df):
    # Calculate the ratio thickness/diameter for the tubes:
    tube_indices = df.loc[df['Preform']=='Tube'].index
    df.loc[tube_indices,'Ratio'] = df.loc[tube_indices, 'Thickness [mm]'] / df.loc[tube_indices,'External diameter [mm]']
    # Convert columns into the correct dtype:
    for T in ['Entry 45°C', 'Entry 60°C', 'Entry 90°C']:
        df[T] = to_datetime(df[T], format='%m/%d/%Y-%H:%M')
    df['Preform status'] = df['Preform status'].astype(str)
    df['Ramping status'] = df['Ramping status'].astype(str)
    df['Final status'] = df['Final status'].astype(str)
    df['Action'] = df['Action'].astype(str)
## Verify the preform manufacturing steps:
def set_preform_status(df):
    for i in df.index:
        # Microstructured fibers:
        if df.loc[i, 'Preform'] == 'Billet':
            if df.loc[i, 'Thread'] == 'OK':
                df.loc[i, 'Preform status'] = 'Thread completed'
            elif df.loc[i, 'Pin'] == 'OK':
                df.loc[i, 'Preform status'] = 'Pin completed'
            elif df.loc[i, 'Main drilling'] == 'OK':
                df.loc[i, 'Preform status'] = 'Main drilling completed'
            elif df.loc[i, 'Support drilling'] == 'OK':
                df.loc[i, 'Preform status'] = 'Support drilling completed'
            elif df.loc[i, 'Recess'] == 'OK':
                df.loc[i, 'Preform status'] = 'Recess completed'
            elif df.loc[i, 'Facing'] == 'OK':
                df.loc[i, 'Preform status'] = 'Facing completed'
            else:
                df.loc[i, 'Preform status'] = 'Cut'
        # Capillaries:
        else:
            df.loc[i, 'Thread'] = '-'
            df.loc[i, 'Pin'] = '-'
            df.loc[i, 'Main drilling'] = '-'
            df.loc[i, 'Support drilling'] = '-'
            df.loc[i, 'Recess'] = '-'
            df.loc[i, 'Facing'] = '-'
            df.loc[i, 'Preform status'] = '-'
## Verify the temperature ramping:
def set_ramping_status(df):
    ramping = {'Short': {'45°C': 1, '60°C': 1, '90°C': 7}, 'Medium': {'45°C': 1, '60°C': 1, '90°C': 28}, 'Long': {'45°C': 7, '60°C': 7, '90°C': 28}}
    now = datetime.now()
    # Indices:
    billet_indices = df.loc[df['Preform'] == 'Billet'].index
    thread_completed = df.loc[df['Thread'] == 'OK'].index
    # Modification:
    for i in df.index:
        # Billet with thread completed or tube:
        if ((i in billet_indices) and (i in thread_completed)) or (i not in billet_indices):
            # 90°C:
            if isnull(df.loc[i, 'Entry 90°C']):
                pass
            elif now - df.loc[i, 'Entry 90°C'] > timedelta(days = ramping[df.loc[i, 'Ramping duration']]['90°C']):
                df.loc[i, 'Ramping status'] = '90°C completed'
                continue
            else:
                df.loc[i, 'Ramping status'] = '90°C incompleted'
                continue
            # 60°C:
            if isnull(df.loc[i, 'Entry 60°C']):
                pass
            elif now - df.loc[i, 'Entry 60°C'] > timedelta(days = ramping[df.loc[i, 'Ramping duration']]['60°C']):
                df.loc[i, 'Ramping status'] = '60°C completed'
                continue
            else:
                df.loc[i, 'Ramping status'] = '60°C incompleted'
                continue
            # 45°C:
            if isnull(df.loc[i, 'Entry 45°C']):
                pass
            elif now - df.loc[i, 'Entry 45°C'] > timedelta(days = ramping[df.loc[i, 'Ramping duration']]['45°C']):
                df.loc[i, 'Ramping status'] = '45°C completed'
                continue
            else:
                df.loc[i, 'Ramping status'] = '45°C incompleted'
                continue
        # Billet with thread incompleted:
        elif (i in billet_indices) and (i not in thread_completed):
            df.loc[i, 'Ramping status'] = 'On hold'
        else:
            pass
## Chose the action to be taken:
def take_action(df):
    # Billet:
    billet_indices = df.loc[df['Preform'] == 'Billet'].index
    for i in billet_indices:
        # Modify the preform:
        if df.loc[i, 'Preform status'] == 'Cut':
            df.loc[i, 'Action'] = 'Do facing'
        elif df.loc[i, 'Preform status'] == 'Facing completed':
            df.loc[i, 'Action'] = 'Do recess'
        elif df.loc[i, 'Preform status'] == 'Recess completed':
            df.loc[i, 'Action'] = 'Do support drilling'
        elif df.loc[i, 'Preform status'] == 'Support drilling completed':
            df.loc[i, 'Action'] = 'Do main drilling'
        elif df.loc[i, 'Preform status'] == 'Main drilling completed':
            df.loc[i, 'Action'] = 'Do Pin'
        elif df.loc[i, 'Preform status'] == 'Pin completed':
            df.loc[i, 'Action'] = 'Do thread'
        # Drying chamber control:
        elif (df.loc[i, 'Preform status'] == 'Thread completed') and (df.loc[i, 'Ramping status'] == '90°C incompleted'):
            df.loc[i, 'Action'] = 'Wait in 90°C'
        elif (df.loc[i, 'Preform status'] == 'Thread completed') and (df.loc[i, 'Ramping status'] == '60°C completed'):
            df.loc[i, 'Action'] = 'Move to 90°C'
        elif (df.loc[i, 'Preform status'] == 'Thread completed') and (df.loc[i, 'Ramping status'] == '60°C incompleted'):
            df.loc[i, 'Action'] = 'Wait in 60°C'
        elif (df.loc[i, 'Preform status'] == 'Thread completed') and (df.loc[i, 'Ramping status'] == '45°C completed'):
            df.loc[i, 'Action'] = 'Move to 60°C'
        elif (df.loc[i, 'Preform status'] == 'Thread completed') and (df.loc[i, 'Ramping status'] == '45°C incompleted'):
            df.loc[i, 'Action'] = 'Wait in 45°C'
        # Pulling action decision:
        elif (df.loc[i, 'Preform status'] == 'Thread completed') and (df.loc[i, 'Ramping status'] == '90°C completed'):
            if df.loc[i, 'Stage'] == 'Preform':
                df.loc[i, 'Action'] = 'Pull 1st stage'
            elif df.loc[i, 'Stage'] == '1st stage':
                df.loc[i, 'Action'] = 'Pull 2nd stage'
        else:
            df.loc[i, 'Action'] = 'None'
    # Tube:
    tube_indices = df.loc[df['Preform'] == 'Tube'].index
    for i in tube_indices:
        if df.loc[i, 'Ramping status'] == '90°C completed':
            df.loc[i, 'Action'] = 'Pull 2nd stage'
        elif df.loc[i, 'Ramping status'] == '90°C incompleted':
            df.loc[i, 'Action'] = 'Wait in 90°C'
        elif df.loc[i, 'Ramping status'] == '60°C completed':
            df.loc[i, 'Action'] = 'Move to 90°C'
        elif df.loc[i, 'Ramping status'] == '60°C incompleted':
            df.loc[i, 'Action'] = 'Wait in 60°C'
        elif df.loc[i, 'Ramping status'] == '45°C completed':
            df.loc[i, 'Action'] = 'Move to 60°C'
        elif df.loc[i, 'Ramping status'] == '45°C incompleted':
            df.loc[i, 'Action'] = 'Wait in 45°C'
        else:
            df.loc[i, 'Action'] = 'None'
## Set the final status:
def set_final_status(df):
    df.loc[df['Action'] == 'None', 'Final status'] = 'Completed'
    df.loc[df['Final status'] != 'Completed', 'Final status'] = 'Incompleted'      
## Pos configuration:
def pos_config(df):
    # Convert datetime to string:
    for T in ['Entry 45°C', 'Entry 60°C', 'Entry 90°C']:
        df[T] = df[T].dt.strftime('%m/%d/%Y-%H:%M')
    # Show the final data frame:
    print('Final data frame:')
    print(df)
    print()
    # Ask if the user wants to save the data frame:
    while True:
        question = input('Do you want to save the data frame? [y/n]')
        try:
            if question not in ['y', 'n']:
                raise ValueError('Invalid answer!')
            else:
                save = question
        except ValueError as ve:
            print(ve)
        else:
            break
    # Will save the data frame: 
    if save == 'y':
        # Remove the completed samples:
        df = df[df['Final status'] == 'Incompleted']
        # Write the Excel sheet:
        with ExcelWriter(join(folder, 'Samples Drying Chamber.xlsx'), engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
    # Won't save:
    else:
        pass
## Analyse the actions:
def analyse_actions(df):
    # Actions:
    series = df['Action'].value_counts()
    print('Actions:')
    print(series)
    print()
    labels, values = series.index, series.values
    colors = []
    for i in range(len(labels)):
        # Generate a random color in hexadecimal format:
        color = "#{:06x}".format(randint(0, 0xFFFFFF)) # Generates a random integer between 0 and 16777215
        colors.append(color)
    # Plot:
    fig, ax = subplots(nrows=1, ncols=1, layout='constrained')
    ax.set_title('Actions', loc='center', fontsize=16)
    ax.set_ylabel('Frequency', loc='center', fontsize=12)
    ax.bar(x=labels, height=values, color=colors)
    show()
    # Ask if the user wants to save the graphic:
    while True:
        question = input('Do you want to save the graphics? [y/n]')
        try:
            if question not in ['y', 'n']:
                raise ValueError('Invalid answer!')
            else:
                save = question
        except ValueError as ve:
            print(ve)
        else:
            break
    # Will save the graphic:
    if save == 'y':
        fig.savefig(join(folder, 'Graphic - Counts of Actions'))
    # Won't save:
    else:
        pass  
## Ask if the user wants to stop the program: 
def ask_stop():
    while True:
        # Aks about the stop:
        question = input('Do you want to stop the program? [y/n]')
        try:
            if question not in ['y', 'n']: # Invalid answer.
                raise ValueError('Invalid answer!')
            elif question == 'y':  # Will stop.
                stop = True
            else: # Won't stop.
                stop = False
        except ValueError as ve: # It occured an error.
            print(ve)
        else: # It ran smoothly.
            break
    # Give time for the user to modify the data frame:
    if not stop:
        question = input('Type anything when you are done changing the data sheet: ') 
    else:
        pass
    return stop
## Main control function:
def main():
    # Welcome the user to the program:
    intro()
    # Get the folder path:
    get_folder()
    stop = False
    while not stop:
        # Read the sample informations and their group specifications:
        df = read_excel(join(folder, 'Samples Drying Chamber.xlsx')) # Drying chamber info.
        # Samples control:
        pre_config(df)
        set_preform_status(df)
        set_ramping_status(df)
        take_action(df)
        set_final_status(df)
        pos_config(df)
        # Classification:
        analyse_actions(df)
        # Ask if the user wants to stop the program:
        stop = ask_stop()

# Run the program:
main()
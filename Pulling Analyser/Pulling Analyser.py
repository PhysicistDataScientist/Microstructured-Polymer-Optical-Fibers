# Comments:
'''
None.
'''

# Libraries:
from os import listdir
from os.path import join, exists
from chardet import detect
from pandas import read_csv, DataFrame, ExcelWriter
from matplotlib.pyplot import subplots, show

# Classes:
class Band:
    # Initialize the object:
    def __init__(self, band):
        # Mandatory attributes:
        self.band = band 
        # Data frames:
        self.df = DataFrame() # General data.
        self.df_stats = DataFrame() # Statistics. 
    # Individual analysis:
    def individual_analysis(self, data_path, fig_tab, save):        
        self.df = read_csv(data_path, sep=',', decimal='.')
        while True:
            question = input(f'Do you want to select an interval of fiber band {self.band}? [y/n]')
            try:
                if question not in ['y', 'n']:
                    raise ValueError('Invalid answer!')
                else:
                    break
            except ValueError as ve:
                print(ve)
        if question == 'y': # Will select a region.
            while True:
                t_list = input('Give the time interval endpoints: [t_min,t_max]')
                endpoints = list()
                try:
                    if t_list.count(',') != 1:
                        raise ValueError('Mismatch of itens given!')
                    t_min, t_max = t_list.split(',')
                    for t in [t_min, t_max]:
                        if not t.replace('.','').isdigit():
                            raise ValueError('Not a number!')
                        t = float(t)
                        if t < 0:
                            raise ValueError('Negative time!')
                        endpoints.append(t)
                except ValueError as ve:
                    print(ve)
                else:
                    break
            self.df = self.df[self.df['Time [min]'] >= endpoints[0]]
            self.df = self.df[self.df['Time [min]'] <= endpoints[1]]
        else: # Won't select a region.
            pass
        x = self.df.loc[:, 'Time [min]'].values
        for name in self.df.columns[1:]:
            y = self.df.loc[:, name].values
            if '[C]' in name:
                name = name.replace('[C]', '[°C]')
            # Figure:
            if fig_tab: # Will create the graphics:
                fig, ax = subplots(nrows=1, ncols=1, layout='constrained', figsize=(6,4))
                ax.set_xlabel(self.df.columns[0], loc='center', fontsize=12)
                ax.set_ylabel(name, loc='center', fontsize=12)
                ax.scatter(x, y, s=40, c='black')
                graphic_name = f'Graphic Band {self.band} - ' + name.split('[')[0].strip() + '.png'
                show()
                if save: # Will save.
                    fig.savefig(join(sample_folder, graphic_name))
                else:
                    pass # Won't save.
            else: # Won't create the graphics.
                pass
        if fig_tab: # Will create the table:
            self.df_stats = self.df.describe()
            display(self.df_stats)
            if save: # Will save:
                table_name = f'Table Band {self.band}.xlsx'
                with ExcelWriter(join(sample_folder, table_name), engine='openpyxl') as writer:
                    self.df_stats.to_excel(writer)
            else: # Won't save.
                pass
        else: # Won't create the table.
            pass
    # Comparison between bands of the same sample:
    def compared_bands_analysis(objects, fig_tab, save):
        # Get the columns to be compared:
        possible_names = [column.split('[')[0].rstrip() for column in objects[0].df.columns[1:]] 
        print(f'You can choose the following graphics for comparison:')
        [print(pos) for pos in possible_names]
        while True:
            names_input = input('Type the graphics to be used in the comparison: [Diameter,Temperature]').split(',')
            names = list()
            try:
                for name in names_input:
                    if name not in possible_names:
                        raise FileExistsError('Invalid graphic!')
                    else:
                        names.append(name)
            except FileExistsError as fee:
                print(fee)
            else:
                break
        # Compare samples:
        for name in names:
            for col in objects[0].df.columns[1:]: 
                if name not in col:
                    continue
                else:
                    column = col
                    break
            if fig_tab: # Will plot.
                fig, ax = subplots(nrows=1, ncols=1, layout='constrained', figsize=(6,4))
                ax.set_xlabel('Time [min]', loc='center', fontsize=12)
                ax.set_ylabel(column, loc='center', fontsize=12)
                for object in objects:
                    x, y = object.df.loc[:, 'Time [min]'].values, object.df.loc[:, column].values
                    ax.scatter(x, y, s=40, label=f'Band {object.band}')
                ax.legend(loc='best', fontsize=10)
                show()
                bands_string = ','.join([object.band for object in objects])
                if save: # Will save the plot.
                    fig.savefig(join(sample_folder, 'Graphic Bands '+ bands_string + f' - {name}'))
                else: # Won't save the plot.
                    pass
            else: # Won't plot.
                pass

# Function:
## Introduction to the program:
def intro():
    # Present the program:
    print('--------------------------------------')
    print('Welcome to the "Pulling Control"!')
    print('--------------------------------------')
    print()
    print('Here you will be able to analyse the optical fiber fabrication process.')
    print()
    print('Let\'s start!')
    print()
## Find the path to the sample files: 
def get_sample_folder():
    # Read data:
    while True:
        with open("Pulling Path Manager.txt", mode='rt') as f:
            folder = f.read()
            f.close()
        try: 
            if not exists(folder):
                raise FileExistsError('There is no folder with such path!')
            else:
                break
        except FileExistsError as fee:
            print(fee)
            print('Go to the "Pulling Path Manager.txt" and change its content!')
            print()
            input('Type anything when you are done: ')
    # Get the sample's folder path:
    global sample_folder
    while True:
        # Get the sample's number:
        while True:
            n_sample = input('Sample\'s number: ')
            try:
                if not n_sample.lstrip('-').isdigit():
                    raise ValueError('It is not a number!')
                elif '-' in n_sample:
                    raise ValueError('Negative integers are not allowed!')
                elif ',' in n_sample:
                    raise ValueError('Not integer numbers are not allowed!')
                n_sample = int(n_sample)
                if n_sample == 0:
                    raise ValueError('There is no fiber label 0!')
                else:
                    break
            except ValueError as ve:
                print(ve)
        # Join the folder with the sample identification suffix:
        sample_folder = join(folder, f'E - {n_sample}')
        try:
            if not exists(sample_folder):
                raise FileExistsError("Invalid fiber type or sample's number!")
            else:
                break
        except FileExistsError as fee:
            print(fee)
## Decide if it is necessary to create plots, tables and saving them:
def ask_create_save():
    # Decide if it is necessary to create plots and tables:
    while True:
        # Aks the operation mode:
        question = input('Do you want to create plots and tables?: [y/n]')
        try:
            if question not in ['y', 'n']: # Invalid answer.
                raise ValueError('Invalid answer!')
            elif question == 'y': # Positive answer.
                fig_tab = True
            else: # Negative answer.
                fig_tab = False 
        except ValueError as ve: # It occured an error.
            print(ve)
        else: # It ran smoothly.
            break
    # Decide if it is necessary to save plots and tables:
    if fig_tab: # Will create.
        while True:
            # Aks the operation mode:
            question = input('Do you want to save plots and tables?: [y/n]')
            try:
                if question not in ['y', 'n']: # Invalid answer.
                    raise ValueError('Invalid answer!')
                elif question == 'y': # Positive answer.
                    save = True
                else: # Negative answer.
                    save = False 
            except ValueError as ve: # It occured an error.
                print(ve)
            else: # It ran smoothly.
                break
    else: # Won't create.
        save = False
    return fig_tab, save
## Select the bands to be analised:
def select_bands_analyse(possible_bands):
    while True:
        question = input('Give a list with the optical bands to be analysed individually: [A,B]')
        band_list = list()
        try:
            if ',' not in question: # One band.
                if question == 'Trash':
                    ExcelWriter.append(question)
                elif (not question.isalpha()) or (not question.isupper() or (len(question) > 1)):
                    raise ValueError('Invalid band!')
                elif question not in possible_bands:
                    raise FileExistsError('There is no such available band!')
                else:
                    band_list.append(question)
            else: # More than one band.
                bands = question.split(',')
                for ques in bands:
                    if ques == 'Trash':
                        band_list.append(ques)
                    elif (not ques.isalpha()) or (not ques.isupper()) or (len(ques) > 1):
                        raise ValueError('Invalid band!')
                    elif ques not in possible_bands:
                        raise FileExistsError('There is no such available band!')
                    else:
                        band_list.append(ques)
        except ValueError as ve:
            print(ve)
        except FileExistsError as fe:
            print(fe)
        else:
            break
    return band_list
## Individual data file modification:
def modify_file(data_path):
    'Time,Tractor Speed,Preform feed rate,Temperature,Tension,Preform Pressure,Diameter,Diameter X,Diameter Y\n'
    header1 = 'Time,Tractor Speed,Preform feed rate,Temperature,Tension,Preform Pressure,Diameter,Diameter X,Diameter Y\n'
    header2 = 'Time,Capstan speed,Preform feed rate,Temperature,Tension,Preform Pressure,Diameter,Diameter X,Diameter Y\n'
    units = '[min],[m/min],[mm/min],[ºC],[g],[mBar],[mm],[um],[um]\n'
    # Get the file enconding:
    with open(data_path, mode='rb') as f:
        detection = detect(f.read())
        f.close()
    # Read the data:
    with open(data_path, mode='rt', encoding=detection['encoding']) as f:
        rows = f.readlines()
        f.close()
    ## The file need to be modified:
    file = data_path.split('Pulling')[1]
    file = 'Pulling' + file
    if (header1 in rows) or (header2 in rows):
        # Identify the header (tractor/capstan speed):
        if header1 in rows:
            header = header1
        else:
            header = header2
        # Find the header position:
        ind = [i for i, row in enumerate(rows) if row == header]
        ind = ind[0]
        # Put together the header columns and their measurement units:
        tuples = list(zip(header.replace('\n','').split(','), units.replace('\n','').split(',')))
        # Create a new header:
        header = str()
        for i, (param, unity) in enumerate(tuples):
            if unity == '[ºC]':
                unity = '[C]'
            if i == len(tuples) - 1:
                header += f'{param} {unity}\n'
            else:
                header += f'{param} {unity},'
        # Cut off the data above the header (drawing tower information):
        data = str()
        data = ''.join([data + row for i, row in enumerate(rows) if i > ind + 1])
        data = header + data
        with open(data_path, mode='wt') as g:
            g.write(data)
            g.close()
        print(f'Modification on "{file}" is done.')
    ## The file was already modified:
    else:
        print(f'"{file}" is already modified.')
## Ask if the user wants to compare the bands:
def select_bands_compare(bands_to_analyse):
    if len(bands_to_analyse) > 1: # There are more than one band being analysed.
        while True:
            question1 = input('Do you want to compare the data between fiber bands? [y/n]')
            try:
                if question1 not in ['y', 'n']:
                    raise ValueError('Invalid answer!')
                else:
                    pass
            except ValueError as ve:
                print(ve)
            else:
                break
    else: # Just one band being analysed, so none to compare.
        question1 = 'n'
    if question1 == 'y': # Will compare bands.
        while True:
            question2 = input('Give a list with the optical bands to be compared: [A,B]')
            band_list = list()
            try:
                if ',' not in question2: # One band.
                    raise ValueError('You can\'t compare with just one band!')
                else: # More than one band.
                    bands = question2.split(',')
                    for ques in bands:
                        if ques == 'Trash':
                            band_list.append(ques)
                        elif (not ques.isalpha()) or (not ques.isupper()) or (len(ques) > 1):
                            raise ValueError('Invalid band!')
                        elif ques not in bands_to_analyse:
                            raise ValueError('Your band is not being analysed!')
                        else:
                            band_list.append(ques)
            except ValueError as ve:
                print(ve)
            else:
                break
    else: # Won't compared bands.
        print('No comparison between fiber bands was requested.')
        print()
        band_list = list()
    return band_list
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
    return stop
## Main control function:
def main():
    # Introduction:
    intro()
    # Main loop:
    stop = False
    while not stop:
        # Find sample folder:
        get_sample_folder()
        # Access files withing sample folder:
        path_list = [file for file in listdir(sample_folder) if 'Data Pulling Band ' in file]
        # Decide if plotting and showing it is relevant:
        fig_tab, save = ask_create_save()
        # Choose the bands to analyse:
        print('You can analyse the following fiber bands:')
        possible_bands = [path.split('Band')[-1].split('.txt')[0].strip() for path in path_list]
        [print(pos_band) for pos_band in possible_bands]
        print()
        bands_to_analyse = select_bands_analyse(possible_bands)
        # Update the files to be analysed:
        new_path_list = list()
        for path in path_list:
            label = path.split('Band')[-1].split('.txt')[0].strip()
            if label in bands_to_analyse:
                new_path_list.append(path)
        path_list = new_path_list
        print('You chose to analyse the following fiber bands:')
        [print(band) for band in bands_to_analyse]
        print()
        # Create the objects:
        # Analyse each band individually:
        objects = list()
        for path in path_list:
            data_path = join(sample_folder, path)
            # Modify data files:
            modify_file(data_path)
            # Individual analysis:
            band = path.split('Band')[-1].split('.txt')[0].strip()
            object = Band(band=band)
            if band in bands_to_analyse:
                object.individual_analysis(data_path, fig_tab=fig_tab, save=save)
            else:
                pass
            objects.append(object)
        # Decide if you want to compare the bands:
        bands_to_compare = select_bands_compare(bands_to_analyse)
        if len(bands_to_compare) != 0: # Will compare.
            # Compare curves for selected files:
            objects_to_compare = [object for object in objects if object.band in bands_to_compare]
            Band.compared_bands_analysis(objects_to_compare, fig_tab=fig_tab, save=save)
        else: # Won't compare.
            pass
        # Ask if the program shall be interrupted:
        stop = ask_stop()

# Run the program:
main()
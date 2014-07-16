import csv

TRAINED_BRANDS = './data/trained_brands.csv'

def read():
    """
    Load the trained brands and iterate through
    """
    
    with open(TRAINED_BRANDS, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        
        next(csvreader, None)  # skip the headers
        
        for row in csvreader:
            item_type,item_id,item_descriptor,count,username,log_id,major_brand,medium_brand, \
                minor_brand,sub_brand,subsub_brand = row
                
            print item_descriptor, major_brand, count
                    

if __name__ == "__main__":
    read()
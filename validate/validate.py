from forestcost import main_model
import random
import csv

costdata = csv.DictReader(open('cost_data.csv','rb'))

fields = """acres elev slope stand_wkt_dummy RemovalsCT TreeVolCT
          RemovalsSLT TreeVolSLT RemovalsLLT TreeVolLLT
          HdwdFractionCT HdwdFractionSLT HdwdFractionLLT
          PartialCut landing_coords_dummy haulDist haulTime coord_mill_dummy""".split()
          
          # Helicopter = True 
          # HaulProportion = 1.0
          # skid_distance=None

iters = 200

print "name,actual,predicted\n"
for row in costdata:
    row['landing_coords_dummy'] = 'dummy'
    row['coord_mill_dummy'] = 'dummy'
    row['stand_wkt_dummy'] = 'dummy'
    for i in range(iters):
        args = []
        for field in fields:
            val = row[field]
            try:
                val = float(val)
            except ValueError:
                if "|" in val:
                    # randomly sample from uniform distribution
                    low, high = [float(x) for x in val.split("|")]
                    val = random.uniform(low, high)

            args.append(val)

        if row['PartialCut'] == 1:
            haulprop = 0.5
        else:
            haulprop = 1.0

        val = row['skid_distance']
        try:
            skid_distance = float(val)
        except ValueError:
            if "|" in val:
                # randomly sample from uniform distribution
                low, high = [float(x) for x in val.split("|")]
                skid_distance = random.uniform(low, high)

        #print args
        results = main_model.cost_func(*args, Helicopter=False, HaulProportion=haulprop, skid_distance=skid_distance)
        print ",".join(str(x) for x in [row['name'], row['actual_cost'], results['total_cost']])
        print "\n"

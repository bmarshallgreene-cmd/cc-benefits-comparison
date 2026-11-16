import csv,collections
def load(y):
    D=collections.defaultdict(list)
    for r in csv.DictReader(open(f'/home/claude/work/sco/{y}/{y}_CommunityCollegeDistrict.csv',encoding='cp1252',errors='replace')):
        for k in ('TotalWages','RegularPay','HealthDentalVision','DefinedBenefitPlanContribution','MinPositionSalary','MaxPositionSalary'):
            try: r[k]=float(r[k] or 0)
            except ValueError: r[k]=0.0
        D[r['EmployerName'].replace(' Community College District','').replace(' Joint','')].append(r)
    return D

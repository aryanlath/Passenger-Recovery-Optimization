from feasible_flights import *
from constants import *
from init_functions import *
from gurobi_optimisation import *
from Leap_Quantum_Main import *
import pprint
import constants_immutable
from mailer import *
pp = pprint.PrettyPrinter(indent=4)
from Assign_Class import *


def Main_function():

    # initializes the loyalty scores for the passengers
    # init_loyalty_dictionary()

    # global all_flights, pnr_objects,  pnr_flight_mapping, pnr_to_s2
    constants_immutable.all_flights, constants_immutable.pnr_objects, constants_immutable.pnr_flight_mapping, constants_immutable.pnr_to_s2 = Get_All_Maps()
    # finds the normalization factors for the cost function
    init_normalize_factors()
    


    # Identify the impacted PNRs
    Impacted_PNR = Get_Impacted_passengers(constants_immutable.all_flights, constants_immutable.pnr_objects)


    print("Total impacted Passengers: ",len(Impacted_PNR))
    pp.pprint(Impacted_PNR)

    # Classical part
    # start = time.time()
    # result = optimize_flight_assignments(Impacted_PNR)
    # end = time.time()
    # print("Total Classical Time:" , end-start)
    # print()
    # print("Total Reassigned: ",len(result['Assignments']))
    # print("Classical Optimal Cost",result['Total Cost'])
    # pp.pprint(result['Assignments'])
    # print("Not Assigned PNRs: ")
    # pp.pprint(result['Non Assignments'])
    # print("#"*100)
    # print()

   # Quantum Pipeline
    start = time.time()
    quantum_result =quantum_optimize_flight_assignments(Impacted_PNR,QSol_count=4)
    end = time.time()
    print("Total Quantum Time:", end-start)
    print()
    print("Total Reassigned: ",len(quantum_result[0]['Assignments']))
    pp.pprint(quantum_result[0]['Assignments'])
    print("Not Assigned PNRs: ")
    pp.pprint(quantum_result[0]['Non Assignments'])
    print("#"*100)
    print()


    # # Constructing 3 CSVs corresponding to the top 3 quantum solutions
    # for idx in range(0,len(quantum_result)):
    #     result_new=Cabin_to_Class(quantum_result[idx]["Assignments"])
    #     result_new_modified = []
    #     for T in result_new :
    #         Cancelled_Flights = []
    #         for inv in T[0].inv_list:
    #             if(constants_immutable.all_flights[inv].status=="cancelled"):
    #                 Cancelled_Flights.append(constants_immutable.all_flights[inv])
                    
    #         result_new_modified.append((T[0].pnr_number,T[0].email_id,T[1],T[2],T[3],Cancelled_Flights))
    #     df_assignments = pd.DataFrame(result_new_modified, columns=['PNR_Number', 'PNR_Email','Flight', 'Cabin','Class','Cancelled Flights'])
    #     df_non_assignments = pd.DataFrame(quantum_result[idx]['Non Assignments'], columns=['PNR_Number'])

    #     df_assignments.to_csv(f"Results/assignments_{idx}.csv")
    #     df_non_assignments.to_csv(f"Results/non_assignments_{idx}.csv")
    
    
    
    
    # Network flow pipeline
    start=time.time()
    final_result = Cabin_to_Class(result["Assignments"])
    end=time.time()
    print("Network Flow time :",end-start)
    print()
    pp.pprint(final_result)
    print("#"*100)
    print()

    # Exception List Handling
    start=time.time()
    city_pairs_result = optimize_flight_assignments(result['Non Assignments'],True)
    end=time.time()
    print("Exception Handling time: ",end-start)
    print()
    print("Total Assignments with different City-Pairs: ", len(city_pairs_result['Assignments']))
    pp.pprint(city_pairs_result['Assignments'])
    print("Not Assigned PNRs: ")
    pp.pprint(city_pairs_result['Non Assignments'])
    print("#"*100)
    print()
    

    # send emails
    #send_mail("Results/assignments.csv")

if __name__==  "__main__":
    Main_function()

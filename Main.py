import pandas as pd
import streamlit as st

def calculation(cofounders, anti_dulations, pre_money_valuation,investments, total_number_of_shares_count):

    total_number_of_shares_percent = sum(cofounders)

    if total_number_of_shares_percent != 100:
        st.error('You have entered wrong values for founder percentages. Please ensure they add up to 100%.')
        return None
    
    if pre_money_valuation == 0:
        st.error('You Have to Fill Pre Money Valuation Input.')
        return None
    
    if investments == 0:
        st.error('You Have to Fill Investmnets Input.')
        return None
    
    if total_number_of_shares_count == 0:
        st.error('You Have to fill Total Number of Shares Input.')
        return None

    post_money_valuation = pre_money_valuation + investments

    price_per_share = pre_money_valuation / total_number_of_shares_count

    new_shares = investments / price_per_share

    total_number_of_shares_afte_financing = total_number_of_shares_count + new_shares

    number_of_shares = []

    for i in range(len(cofounders)) :
        ns = (cofounders[i] /100 ) * total_number_of_shares_count
        number_of_shares.append(ns)

    for j in range(len(cofounders)):
        if anti_dulations[j] ==1:
            number_of_shares[j] = (cofounders[j] / 100) * total_number_of_shares_afte_financing

    new_investor = new_shares

    sum_of_shares = sum(number_of_shares) + new_investor

    new_investor = new_investor - (sum_of_shares - total_number_of_shares_afte_financing)

    sum_of_shares = sum(number_of_shares)  + new_investor

    fdx = []

    for i in range(len(cofounders)):

        fdi = number_of_shares[i] / total_number_of_shares_afte_financing

        fdx.append(fdi)


    FD_ni = new_investor / total_number_of_shares_afte_financing

    fdx.append(FD_ni)

    FDs = [round(fd * 100) for fd in fdx]

    number_of_shares.append(new_investor)  

    teams = []

    for j in range(len(cofounders)):
        cofounder_no = 'Co_founder' + str(j+1)
        teams.append(cofounder_no) 

    teams.append('New_investor')

    results = {
        'New_team': teams,
        'Number_of_shares': number_of_shares,
        'FD %':FDs
    }

    df = pd.DataFrame(results)

    return df



def main():
    logo_path = 'easycapraise-social-image.png'
    st.image(logo_path, width = 300)
    result_df = None 
    st.title("Valuation Calculator")
    
    number_of_cofounders = st.number_input('# How Many Co Founders Are There? ' ,min_value=1, max_value=100, step=1)
    
    if number_of_cofounders >0:
        cofounders = [st.number_input(f'Co Founder #{i + 1} Percentage (%):', min_value=0, max_value=100, step=5) for i in range(number_of_cofounders)]

        st.markdown('<span style="color:orange;font-weight:bold">* Please Check the Checkbox if you want to Assign Any Anti Dilution Value To each Co Founder.</span>', unsafe_allow_html=True)
        anti_dulations = [st.checkbox(f'Anti Dilution for Co Founder #{i + 1}') for i in range(number_of_cofounders)]


        pre_money_valuation = st.number_input('Enter Pre Money Valuation:', min_value=0, step=100000,format="%d")
        investments = st.number_input('Enter Investment:', min_value=0, step=100000,format="%d")
        total_number_of_shares_count = st.number_input('Enter Total Number of Shares:', min_value=0, step=100000,format="%d")

        if st.button('Calculate'): 
            anti_dulations_values = [checkbox for checkbox in anti_dulations]

            result_df = calculation(cofounders, anti_dulations_values, pre_money_valuation, investments, total_number_of_shares_count)

        if result_df is not None:
                num_Sum = result_df['Number_of_shares'].sum()
                st.write(result_df)
            
                st.markdown(f'* The Total Amount for Number of Shares is:<span style="color:green;font-weight:bold"> {num_Sum} </span>', unsafe_allow_html=True)

                csv_file = result_df

                csv_file = result_df.to_csv(index=False)
                
                st.download_button(

                    label="Download CSV",
                    data=csv_file,
                    file_name="Valuation_results.csv",
                    key="download-btn"
                )
        
    
if __name__ == "__main__":
    main()


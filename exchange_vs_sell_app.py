import streamlit as st


def main():
    st.title("1031 Exchange vs. Paying Capital Gains Tax Today")

    st.markdown(
        """
    ## Investment Options Comparison

    **Option 1**: Sell the property, pay capital gains tax today, and invest the net proceeds at a specified annual return.

    **Option 2**: Perform a 1031 exchange into a Delaware Statutory Trust (DST), avoid paying capital gains tax now, and receive total annual returns (including cash flow and appreciation).

    Adjust the parameters below to see how the results change.
    """
    )

    # Input parameters
    st.sidebar.header("Input Parameters")

    # Add equity input that syncs with property value and cost basis
    equity = st.sidebar.number_input(
        "Equity in Property",
        value=400000,
        min_value=0,
        step=10000,
        format="%d",
        help="Your equity in the property (property value minus debt)",
    )

    initial_property_value = st.sidebar.number_input(
        "Initial Property Value",
        value=equity + 600000,  # Default to equity + some assumed debt
        min_value=equity,  # Property value must be at least the equity amount
        step=10000,
        format="%d",
        help="Current market value of the property",
    )

    cost_basis = st.sidebar.number_input(
        "Cost Basis of the Property",
        value=initial_property_value - equity,  # Default to property value minus equity
        min_value=0,
        max_value=initial_property_value,  # Cost basis cannot exceed property value
        step=10000,
        format="%d",
        help="Original purchase price plus improvements",
    )

    # Add dollar sign and commas to the labels
    st.sidebar.markdown(f"**Equity:** ${equity:,}")
    st.sidebar.markdown(f"**Property Value:** ${initial_property_value:,}")
    st.sidebar.markdown(f"**Cost Basis:** ${cost_basis:,}")

    capital_gains_tax_rate = (
        st.sidebar.slider(
            "Capital Gains Tax Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=30.0,
            step=0.1,
        )
        / 100.0
    )
    investment_horizon = st.sidebar.slider(
        "Investment Horizon (years)", min_value=1, max_value=30, value=7, step=1
    )
    option1_return_rate = (
        st.sidebar.slider(
            "Option 1 Investment Annual Return (%)",
            min_value=0.0,
            max_value=20.0,
            value=10.0,
            step=0.1,
        )
        / 100.0
    )
    option2_return_rate = (
        st.sidebar.slider(
            "Option 2 DST Annual Return (%)",
            min_value=0.0,
            max_value=20.0,
            value=12.0,
            step=0.1,
        )
        / 100.0
    )

    st.write("---")

    # Display Capital Gains prominently before the options
    st.header("Capital Gains Analysis")
    capital_gain = initial_property_value - cost_basis
    initial_tax = capital_gain * capital_gains_tax_rate

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Capital Gains", f"${capital_gain:,.2f}")
    with col2:
        st.metric("Capital Gains Tax Rate", f"{capital_gains_tax_rate*100:.1f}%")
    with col3:
        st.metric("Tax if Sold Today", f"${initial_tax:,.2f}")

    st.write("---")

    # Option 1 Calculations
    capital_gain = initial_property_value - cost_basis
    option1_tax_initial = capital_gain * capital_gains_tax_rate
    option1_net_proceeds_initial = initial_property_value - option1_tax_initial
    option1_future_value = (
        option1_net_proceeds_initial * (1 + option1_return_rate) ** investment_horizon
    )
    option1_gain = option1_future_value - option1_net_proceeds_initial
    option1_tax_on_gain = option1_gain * capital_gains_tax_rate
    option1_net_proceeds_final = option1_future_value - option1_tax_on_gain

    # Option 2 Calculations
    option2_net_proceeds_initial = initial_property_value
    option2_future_value = (
        option2_net_proceeds_initial * (1 + option2_return_rate) ** investment_horizon
    )
    option2_gain = option2_future_value - cost_basis
    option2_tax_on_gain = option2_gain * capital_gains_tax_rate
    option2_net_proceeds_final = option2_future_value - option2_tax_on_gain

    # Display Results
    st.header("Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Option 1: Sell and Invest")
        st.write(f"**Initial Net Proceeds:** ${option1_net_proceeds_initial:,.2f}")
        st.write(f"**Future Value Before Tax:** ${option1_future_value:,.2f}")
        st.write(f"**Capital Gains Tax on Gain:** ${option1_tax_on_gain:,.2f}")
        st.write(f"**Net Proceeds After Tax:** ${option1_net_proceeds_final:,.2f}")

    with col2:
        st.subheader("Option 2: 1031 Exchange into DST")
        st.write(f"**Initial Investment:** ${option2_net_proceeds_initial:,.2f}")
        st.write(f"**Future Value Before Tax:** ${option2_future_value:,.2f}")
        st.write(f"**Capital Gains Tax on Gain:** ${option2_tax_on_gain:,.2f}")
        st.write(f"**Net Proceeds After Tax:** ${option2_net_proceeds_final:,.2f}")

    # Determine which option yields higher net proceeds
    if option1_net_proceeds_final > option2_net_proceeds_final:
        difference = option1_net_proceeds_final - option2_net_proceeds_final
        st.success(
            f"**Option 1 yields higher net proceeds by ${difference:,.2f} after taxes.**"
        )
    else:
        difference = option2_net_proceeds_final - option1_net_proceeds_final
        st.success(
            f"**Option 2 yields higher net proceeds by ${difference:,.2f} after taxes.**"
        )

    # Plot the results
    st.write("---")
    st.subheader("Net Proceeds Comparison")
    import pandas as pd
    import altair as alt

    data = pd.DataFrame(
        {
            "Option": ["Option 1", "Option 2"],
            "Net Proceeds After Tax": [
                option1_net_proceeds_final,
                option2_net_proceeds_final,
            ],
        }
    )

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x="Option",
            y="Net Proceeds After Tax",
            tooltip=["Option", "Net Proceeds After Tax"],
        )
        .properties(width=600, height=400)
    )

    st.altair_chart(chart)

    # Show Data Table
    st.write("---")
    st.subheader("Detailed Calculations")
    detailed_data = {
        "Description": [
            "Initial Property Value",
            "Cost Basis",
            "Total Capital Gains",
            "Current Capital Gains Tax",
            "Equity in Property",
            "Capital Gains Tax Rate",
            "Investment Horizon",
            "Option 1 Initial Net Proceeds",
            "Option 1 Future Value Before Tax",
            "Option 1 Capital Gains Tax on Gain",
            "Option 1 Net Proceeds After Tax",
            "Option 2 Initial Investment",
            "Option 2 Future Value Before Tax",
            "Option 2 Capital Gains Tax on Gain",
            "Option 2 Net Proceeds After Tax",
        ],
        "Value": [
            f"${initial_property_value:,.2f}",
            f"${cost_basis:,.2f}",
            f"${capital_gain:,.2f}",
            f"${initial_tax:,.2f}",
            f"${equity:,.2f}",
            f"{capital_gains_tax_rate * 100:.2f}%",
            f"{investment_horizon} years",
            f"${option1_net_proceeds_initial:,.2f}",
            f"${option1_future_value:,.2f}",
            f"${option1_tax_on_gain:,.2f}",
            f"${option1_net_proceeds_final:,.2f}",
            f"${option2_net_proceeds_initial:,.2f}",
            f"${option2_future_value:,.2f}",
            f"${option2_tax_on_gain:,.2f}",
            f"${option2_net_proceeds_final:,.2f}",
        ],
    }
    df_details = pd.DataFrame(detailed_data)
    st.table(df_details)


if __name__ == "__main__":
    main()

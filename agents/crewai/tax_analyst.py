// CrewAI crew: tax-analyst
// Reviews the creator's tax situation, identifies deductions, and files forms.

# /// script
# requires-python = ">=3.12"
# dependencies = ["crewai>=0.51"]
# ///

from crewai import Agent, Task, Crew

tax_analyst = Agent(
    role="Tax Analyst",
    goal="Identify deductions and file tax forms for the creator",
    backstory="You are a CPA with 20 years of experience in US/UK/EU tax.",
    allow_delegation=False,
)

compliance_officer = Agent(
    role="Compliance Officer",
    goal="Verify that all filings meet regulatory requirements",
    backstory="You are a former IRS agent and GDPR DPO.",
    allow_delegation=False,
)

kyc_reviewer = Agent(
    role="KYC Reviewer",
    goal="Verify creator identity and ensure all required KYC docs are present",
    backstory="You are a former bank compliance officer.",
    allow_delegation=True,
)

analyze = Task(
    description="Analyze the creator's payouts and identify all available deductions for {year} in {jurisdiction}.",
    expected_output="A list of deductions with the legal basis for each.",
    agent=tax_analyst,
)

file = Task(
    description="File the appropriate 1099/W-8BEN/VAT MOSS form based on the analysis.",
    expected_output="A signed PDF URL and an audit-log entry.",
    agent=tax_analyst,
)

verify = Task(
    description="Verify the filing against regulatory requirements.",
    expected_output="A compliance check report.",
    agent=compliance_officer,
)

crew = Crew(
    agents=[tax_analyst, compliance_officer, kyc_reviewer],
    tasks=[analyze, file, verify],
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff(inputs={"year": 2026, "jurisdiction": "US"})
    print(result)

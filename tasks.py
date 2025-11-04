"""
Legal Research Tasks
"""
from crewai import Task
from textwrap import dedent
from typing import List, Optional

class LegalResearchTasks:
    """
    Task definitions for legal research workflow
    """
    
    def __tip_section(self):
        return "If you deliver exceptional, thorough, and accurate legal research, you'll be highly valued!"
    
    def analyze_case_task(self, agent, case_text: str, specific_queries: Optional[List[str]] = None):
        """
        Task 1: Analyze the case document and extract key information
        """
        queries_text = ""
        if specific_queries:
            queries_text = "\n\nSpecific Questions to Address:\n" + "\n".join(
                f"- {q}" for q in specific_queries
            )
        
        return Task(
            description=dedent(f"""
                **Task**: Comprehensive Case Analysis
                
                **Description**: 
                You must thoroughly analyze the provided case document and extract all critical information.
                This analysis will form the foundation for all subsequent research tasks.
                
                **Case Text**:
                {case_text}
                {queries_text}
                
                **Your Analysis Must Include**:
                
                1. **Parties Identification**:
                   - Identify Petitioner/Plaintiff/Appellant
                   - Identify Respondent/Defendant/Appellee
                   - Note any other relevant parties (witnesses, interveners, etc.)
                   - Describe the relationship between parties
                
                2. **Case Facts Summary**:
                   - Provide a clear, chronological summary of what happened
                   - Include all material facts
                   - Note any disputed facts
                   - Highlight facts that may have legal significance
                
                3. **Legal Issues Identification**:
                   - List all legal issues and questions raised
                   - Identify the main issue and subsidiary issues
                   - Frame each issue as a clear legal question
                   - Prioritize issues by importance
                
                4. **Case Type Classification**:
                   - Determine if this is: Criminal, Civil, Constitutional, Contract, 
                     Property, Company, Consumer, Labour, Family, Tax, or Other
                   - Explain why you classified it this way
                
                5. **Mentioned Legal Provisions**:
                   - List any statutes, sections, or articles mentioned in the case
                   - Note any precedents or case law referred to
                   - Identify any legal doctrines or principles mentioned
                
                6. **Key Details**:
                   - Extract important dates
                   - Note monetary amounts involved
                   - Identify any time limitations or deadlines
                   - Note jurisdiction and court level
                
                **Use the Legal Entity Extractor and other analysis tools available to you.**
                
                **Note**: {self.__tip_section()}
            """),
            agent=agent,
            expected_output=dedent("""
                A comprehensive case analysis report in markdown format containing:
                
                # CASE ANALYSIS REPORT
                
                ## 1. PARTIES INVOLVED
                - Detailed identification of all parties and their roles
                
                ## 2. CASE FACTS SUMMARY
                - Clear chronological summary of events (300-500 words)
                
                ## 3. LEGAL ISSUES IDENTIFIED
                - Numbered list of all legal issues as clear questions
                - Main issue clearly highlighted
                
                ## 4. CASE CLASSIFICATION
                - Case type with explanation
                
                ## 5. MENTIONED LEGAL REFERENCES
                - All statutes, sections, and precedents mentioned
                
                ## 6. CRITICAL DETAILS
                - Dates, amounts, jurisdiction, etc.
                
                ## 7. RESEARCH DIRECTION
                - Suggested areas for statutory and precedent research
            """)
        )
    
    def research_statutes_task(self, agent, case_analysis_context: str = ""):
        """
        Task 2: Research relevant statutory provisions
        """
        return Task(
            description=dedent(f"""
                **Task**: Focused Statutory Research
                
                **Description**:
                Based on the case analysis, find the most relevant statutory provisions. 
                Focus on quality over quantity - find the 5-10 MOST relevant provisions.
                
                **Context from Case Analysis**:
                {{context}}
                
                **Your Research Strategy**:
                
                1. **Identify the primary legal area** (Criminal/Civil/Constitutional/etc.)
                
                2. **Search for main provisions** (do 2-3 focused searches):
                   - First search: Main offense/claim sections
                   - Second search: Procedural provisions
                   - Third search: Any definitions or exceptions
                
                3. **For Each Provision Found**:
                   - Section/Article number
                   - Complete text
                   - Why it's relevant to this case
                   - Key elements or requirements
                
                **Important Instructions**:
                - Do NOT search repeatedly for the same information
                - Once you have 5-10 key provisions, STOP searching
                - Focus on the MOST directly relevant provisions
                - After 3-4 tool uses, provide your final answer
                - Quality matters more than finding every possible provision
                
                **Use your Legal Document Retriever tool efficiently - max 3-4 searches.**
                
                **Note**: {self.__tip_section()}
            """),
            agent=agent,
            expected_output=dedent("""
                A focused statutory research report in markdown format:
                
                # STATUTORY RESEARCH REPORT
                
                ## PRIMARY STATUTORY PROVISIONS
                
                ### 1. [Act Name] - Section/Article [Number]
                **Text**: [Full text]
                **Relevance**: [How it applies to the case]
                **Key Requirements**: [Elements to be proved/met]
                
                ### 2. [Act Name] - Section/Article [Number]
                [Same format]
                
                [Continue for 5-10 most relevant provisions]
                
                ## PROCEDURAL PROVISIONS
                [Key procedural sections if applicable]
                
                ## ANALYSIS
                - How these provisions interact
                - What needs to be established
                - Any defenses or exceptions available
                
                ## RESEARCH NOTES
                - Confidence level: [High/Medium/Low]
                - Any provisions that might need further research
            """),
            context=[case_analysis_context] if case_analysis_context else []
        )
    
    def research_precedents_task(self, agent, case_analysis_context: str = "", statutes_context: str = ""):
        """
        Task 3: Research relevant legal precedents
        """
        return Task(
            description=dedent(f"""
                **Task**: Comprehensive Precedent Research
                
                **Description**:
                Find all relevant case law and precedents that apply to this case. 
                Precedents are crucial as they show how courts have interpreted the law in similar situations.
                
                **Context**:
                {{context}}
                
                **Your Research Must Find**:
                
                1. **Binding Precedents**:
                   - Supreme Court judgments on similar issues
                   - High Court judgments from the relevant jurisdiction
                   - Focus on cases that directly interpret the identified statutes
                
                2. **Persuasive Precedents**:
                   - High Court judgments from other jurisdictions
                   - Well-reasoned decisions that support your analysis
                
                3. **Landmark Cases**:
                   - Find seminal cases that established key legal principles
                   - Cases frequently cited on these issues
                
                4. **Recent Developments**:
                   - Look for recent judgments that may have modified the law
                   - Check if any older precedents have been overruled
                
                **For Each Precedent**:
                - Full case name (Petitioner v. Respondent)
                - Court name (Supreme Court, High Court, etc.)
                - Year and citation if available
                - Brief summary of facts (2-3 sentences)
                - The legal principle established (ratio decidendi)
                - How it applies to the current case
                - Whether it supports or opposes the petitioner's position
                
                **Research Strategy**:
                1. Search Indian Kanoon for cases involving the identified statutes
                2. Use key terms from the issues to find similar cases
                3. Look for cases cited in any precedents mentioned in the original case
                4. Check for cases interpreting the same statutory provisions
                5. Organize by relevance and binding nature
                
                **Use Indian Kanoon Search, Precedent Search, and Web Search tools.**
                
                **Note**: Even if you cannot access full case databases, provide guidance on 
                what types of precedents would be relevant and how to search for them.
                
                **Note**: {self.__tip_section()}
            """),
            agent=agent,
            expected_output=dedent("""
                A comprehensive precedent research report in markdown format:
                
                # PRECEDENT RESEARCH REPORT
                
                ## BINDING PRECEDENTS
                
                ### Supreme Court Judgments
                
                #### 1. [Case Name] ([Year])
                **Citation**: [If available]
                **Court**: Supreme Court of India
                **Facts**: [Brief 2-3 sentence summary]
                **Legal Principle (Ratio Decidendi)**: [The binding principle established]
                **Relevance to Current Case**: [Detailed explanation of how it applies]
                **Position**: [Supports Petitioner/Respondent/Neutral]
                
                [Repeat for each SC judgment]
                
                ### High Court Judgments (Same Jurisdiction)
                [Same format as above]
                
                ## PERSUASIVE PRECEDENTS
                
                ### High Court Judgments (Other Jurisdictions)
                [Same format as above]
                
                ### Landmark Cases
                [Seminal cases establishing important principles]
                
                ## RECENT DEVELOPMENTS
                - Recent cases that may have changed the law
                - Any overruled precedents
                
                ## PRECEDENT ANALYSIS
                - How the case law supports the legal position
                - Any conflicting precedents and how to distinguish them
                - The overall state of the law based on precedents
                
                ## RESEARCH NOTES
                - Search queries used
                - Databases consulted
                - Limitations (if any)
                - Suggestions for further precedent research
            """),
            context=[case_analysis_context, statutes_context] if case_analysis_context and statutes_context else []
        )
    
    def draft_legal_research_report_task(self, agent, case_analysis_context: str = "", 
                                         statutes_context: str = "", precedents_context: str = ""):
        """
        Task 4: Draft comprehensive legal research report
        """
        return Task(
            description=dedent(f"""
                **Task**: Draft Comprehensive Legal Research Report
                
                **Description**:
                Synthesize all research findings into a single, comprehensive, professional legal research report.
                This report will be used by lawyers to understand the case and prepare legal strategy.
                
                **You Have Access To**:
                {{context}}
                
                **Report Structure**:
                
                1. **EXECUTIVE SUMMARY**:
                   - 1-page overview of the case and key findings
                   - Bottom-line legal opinion
                   - Critical recommendations
                
                2. **CASE OVERVIEW**:
                   - Parties involved
                   - Summary of facts
                   - Procedural history (if available)
                
                3. **LEGAL ISSUES**:
                   - Clear statement of each legal issue
                   - Why each issue is important
                
                4. **APPLICABLE STATUTORY FRAMEWORK**:
                   - Organized presentation of all relevant statutes
                   - Group by area of law (Constitutional, Criminal, Civil, etc.)
                   - For each provision: section number, text, and application to case
                
                5. **RELEVANT PRECEDENTS**:
                   - Binding precedents organized by court hierarchy
                   - Key principles from each case
                   - How they apply to current facts
                
                6. **LEGAL ANALYSIS**:
                   - Detailed analysis connecting facts, statutes, and precedents
                   - Discussion of each legal issue
                   - Strengths and weaknesses of legal positions
                   - Counter-arguments and how to address them
                
                7. **LEGAL OPINION**:
                   - Your assessment of the legal merits
                   - Likelihood of success on each issue
                   - Overall legal position
                
                8. **RECOMMENDATIONS**:
                   - Practical next steps
                   - Legal strategy suggestions
                   - Additional research needed (if any)
                   - Procedural considerations
                
                9. **CAVEATS AND LIMITATIONS**:
                   - Note any limitations in the research
                   - Areas of uncertainty
                   - Confidence level in findings
                
                **Writing Guidelines**:
                - Use clear, professional legal language
                - Cite all sources properly
                - Use markdown formatting for readability
                - Be objective and balanced
                - Provide practical, actionable insights
                - Maintain high professional standards
                
                **Note**: {self.__tip_section()}
            """),
            agent=agent,
            expected_output=dedent("""
                A complete, professional legal research report in markdown format with all sections:
                
                # LEGAL RESEARCH REPORT
                
                ## EXECUTIVE SUMMARY
                [Concise overview with key findings and bottom-line opinion]
                
                ## I. CASE OVERVIEW
                ### A. Parties
                ### B. Facts
                ### C. Procedural History
                
                ## II. LEGAL ISSUES
                [Numbered list of all issues]
                
                ## III. APPLICABLE STATUTORY FRAMEWORK
                ### A. Constitutional Provisions
                ### B. Criminal Law
                ### C. Civil Law
                ### D. Specialized Acts
                [For each: Section, Text, Application]
                
                ## IV. RELEVANT PRECEDENTS
                ### A. Supreme Court Judgments
                ### B. High Court Judgments
                ### C. Other Relevant Cases
                [For each: Case details, principle, application]
                
                ## V. LEGAL ANALYSIS
                ### Issue 1: [Issue Statement]
                [Detailed analysis with statutes and precedents]
                ### Issue 2: [Issue Statement]
                [Continue for all issues]
                
                ## VI. LEGAL OPINION
                [Assessment of legal merits and likelihood of success]
                
                ## VII. RECOMMENDATIONS
                [Practical next steps and strategy]
                
                ## VIII. RESEARCH CONFIDENCE AND CAVEATS
                [Limitations and areas for further research]
                
                ---
                **Prepared by**: AI Legal Research System
                **Date**: [Current date]
            """),
            context=[case_analysis_context, statutes_context, precedents_context] if all([case_analysis_context, statutes_context, precedents_context]) else []
        )
    
    def review_research_report_task(self, agent, research_report_context: str = ""):
        """
        Task 5: Quality review of the research report
        """
        return Task(
            description=dedent(f"""
                **Task**: Quality Review of Legal Research Report
                
                **Description**:
                Conduct a thorough quality review of the legal research report to ensure it meets 
                the highest professional standards of accuracy, completeness, and utility.
                
                **Report to Review**:
                {{context}}
                
                **Review Checklist**:
                
                1. **Accuracy Review**:
                   - Are all statute citations correct?
                   - Are precedent names and citations accurate?
                   - Is the legal analysis sound?
                   - Are there any factual errors?
                
                2. **Completeness Review**:
                   - Have all relevant statutes been identified?
                   - Are important precedents missing?
                   - Is each legal issue fully addressed?
                   - Are there gaps in the research?
                
                3. **Clarity Review**:
                   - Is the writing clear and professional?
                   - Is the structure logical?
                   - Are complex concepts explained well?
                   - Is the report easy to navigate?
                
                4. **Practical Utility Review**:
                   - Are the recommendations actionable?
                   - Would this report help a lawyer prepare the case?
                   - Is the legal opinion well-supported?
                   - Are caveats and limitations clearly stated?
                
                5. **Consistency Review**:
                   - Is the analysis internally consistent?
                   - Do conclusions follow from the research?
                   - Are there any contradictions?
                
                **Your Output Should**:
                - Identify any errors or omissions
                - Suggest improvements
                - Highlight strengths
                - Provide an overall quality assessment
                - If the report is excellent, approve it for final delivery
                - If improvements are needed, specify what changes to make
                
                **Note**: {self.__tip_section()}
            """),
            agent=agent,
            expected_output=dedent("""
                A quality review report in markdown format:
                
                # QUALITY REVIEW REPORT
                
                ## OVERALL ASSESSMENT
                [Rating: Excellent/Good/Needs Improvement]
                [Overall comments on quality]
                
                ## ACCURACY REVIEW
                ✓ **Strengths**:
                - [What was accurate and well-done]
                
                ⚠ **Issues Found**:
                - [Any errors or inaccuracies, if any]
                
                ## COMPLETENESS REVIEW
                ✓ **Strengths**:
                - [What was comprehensive]
                
                ⚠ **Gaps Identified**:
                - [Missing provisions or precedents, if any]
                
                ## CLARITY AND STRUCTURE
                ✓ **Strengths**:
                - [What was clear and well-organized]
                
                ⚠ **Areas for Improvement**:
                - [Unclear sections or structural issues, if any]
                
                ## PRACTICAL UTILITY
                ✓ **Strengths**:
                - [Practical and useful aspects]
                
                ⚠ **Suggestions**:
                - [How to make it more useful]
                
                ## SPECIFIC RECOMMENDATIONS
                1. [Specific improvement needed, if any]
                2. [Another improvement, if any]
                
                ## FINAL RECOMMENDATION
                ☐ Approve for delivery - Report meets professional standards
                ☐ Minor revisions needed - [Specify what]
                ☐ Major revisions needed - [Specify what]
                
                ## REVIEWER NOTES
                [Any additional observations or suggestions]
            """),
            context=[research_report_context] if research_report_context else []
        )
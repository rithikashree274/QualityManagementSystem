def first_call_resolution(audio_text:str) -> str:
    return f"""
        First Call Resolution (FCR): Indicates the percentage of calls resolved on the first 
        interaction, showcasing the agent's ability to solve issues efficiently without follow up.
        in a folder the audio which was discussed by problem we want to find whether the problem is solved or not .
        Rate in numbers if solved means give 1 and not solved means give 0.
        {audio_text}
        Rate in numbers if solved means give 1 and not solved means give 0.
        """

def customer_satisfaction_score(audio_text: str) -> str:
    return f"""
        Customer Satisfaction Score (CSAT): A metric derived from customer feedback 
        post-call, reflecting the customer's satisfaction with the service received.
        rate a scale from 1 to 5 due to the customers satisfactions. 
        The given document can be in other languages. Manage accordingly.
        {audio_text}
        give the output in a single number.
        """


def call_transfer_rate(audio_text: str) -> str:
    return f"""
        Call Transfer Rate: Measures how often calls are transferred to another agent or 
        department, which can indicate the need for better first-contact resolution or agent 
        training.
        ---------------------------------
        {audio_text}
        ---------------------------------
        check if the call is transfered or not . in the above sentence
        If transfered means give 1 and not transfered means give 0.
        just give sigle number .not a sentences.
        """


def error_rate(audio_text: str) -> str:
    return f"""
        Error Rate: The frequency of errors made by agents during calls, such as providing 
        incorrect information or failing to follow proper protocols
        ---------------------------------
        {audio_text}
        ---------------------------------
        calculate the error where the sentence that should be corrected while talking and find how many times it should be corrected.
        And give just  single numbers how many times it should be corrected.
        just give sigle number .not a sentences.
        """
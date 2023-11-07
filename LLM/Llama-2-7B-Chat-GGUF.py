from ctransformers import AutoModelForCausalLM

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained(
    "./", model_file="llama-2-7b-chat.Q5_K_S.gguf", model_type="llama", gpu_layers=50
)

print(
    llm(
        "You are a conversational assistant. You should asnwer every question like a real human, like a conversation. User is A and you are B. Answer in two line.\nA: Tell me about the Roman empire.\nB: The Roman Empire was a vast and powerful civilization that ruled much of Europe and North Africa from 27 BC to 476 AD. It was founded by Augustus Caesar and lasted for over four centuries, leaving a lasting legacy in law, architecture, engineering, and governance. A: When it was founded? B:"
    )
)

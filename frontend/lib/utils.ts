export async function getStreamableText(response: unknown): Promise<string> {
  if (!response) return "";
  
  if (typeof response === "string") {
    return response;
  }

  if (response instanceof ReadableStream) {
    const reader = response.getReader();
    const decoder = new TextDecoder();
    let text = "";
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      text += decoder.decode(value, { stream: true });
    }
    
    return text;
  }

  if (typeof response === "object" && response !== null) {
    const obj = response as Record<string, unknown>;
    if ("text" in obj && typeof obj.text === "string") {
      return obj.text;
    }
    if ("content" in obj && typeof obj.content === "string") {
      return obj.content;
    }
  }

  return String(response);
}

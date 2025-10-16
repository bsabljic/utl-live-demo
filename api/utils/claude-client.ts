// api/utils/claude-client.ts
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY!, // dodaj varijablu u Vercel > Settings > Environment Variables
});

export async function askClaude(prompt: string) {
  const res = await anthropic.messages.create({
    model: 'claude-3-haiku-20240307',   // ili drugi dostupan model
    max_tokens: 512,
    messages: [{ role: 'user', content: prompt }],
  });

  // jednostavan extractor teksta
  const first = res.content?.[0];
  if (first && first.type === 'text') {
    // @ts-ignore (ako želiš, možeš tipizirati preciznije)
    return first.text as string;
  }
  return '';
}

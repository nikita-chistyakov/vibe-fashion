import { Camera } from '@/components/camera';
import { Button } from '@/components/ui/button';
import { Conversation } from '@/components/conversation';
import { useConversationStore } from '@/libs/zustand/conversation';
import { Roles } from '@/constants';
import { useInputStore } from '@/libs/zustand/input';
import { useCallback, useState } from 'react';
import { ImagesDisplay } from '@/components/imagesDisplay';
import { Headline } from '@/components/headline';
import { backendPost } from '@/libs/backendPost';
import { Input } from '@/components/ui/input';

export const Pannel = () => {
  const { addMessages, addImagesStored } = useConversationStore();
  const { text, setText, images } = useInputStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = useCallback(
    async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      if (text.trim().length === 0 || images.length === 0) {
        return;
      }
      setIsLoading(true);
      addMessages([{ role: Roles.USER, content: text }]);
      const response = await backendPost({ text, imageBase64: images[0] });
      addMessages([
        {
          role: Roles.ASSISTANT,
          content: response.text ?? 'No response from server',
        },
      ]);
      if (response.images.length > 0) {
        addImagesStored(response.images);
      }
      setText('');
      setIsLoading(false);
    },
    [addMessages, text, setText, images, addImagesStored],
  );

  return (
    <div className="flex flex-row items-start gap-4 p-4 h-full overflow-y-auto">
      <div className="flex flex-col items-center justify-center gap-4 border border-gray-600 rounded-md p-4 min-w-96 bg-gray-100/25">
        <Camera />
        <Conversation />
        <form onSubmit={handleSend} className="flex flex-row w-full gap-4">
          <Input
            type="text"
            placeholder="What can I help you with?"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="border-gray-600"
            disabled={isLoading}
          />
          <Button variant="outline" type="submit" disabled={isLoading}>
            Send
          </Button>
        </form>
      </div>
      <div className="flex flex-col gap-4">
        <Headline />
        <ImagesDisplay />
      </div>
    </div>
  );
};

import Image from 'next/image';
import { useConversationStore } from '@/libs/zustand/conversation';
import { Button } from '@/components/ui/button';

const WIDTH = 320;
const HEIGHT = 180;
export const defaultImage =
  'https://static.wikia.nocookie.net/virtualyoutuber/images/e/e5/Gremlin_Chibidoki_PNG.png/revision/latest?cb=20250311221031';



export const ImagesDisplay = () => {
  const { imagesStored } = useConversationStore();

  if (imagesStored.length === 0) {
    return null;
  }

  return (
    <div className="grid grid-cols-3 gap-4 border border-gray-300 rounded-md p-4">
      {imagesStored.map((image, idx) => (
        <div key={idx}>
          <Image
            src={`data:image/png;base64,${image.base64}`}
            width={WIDTH}
            height={HEIGHT}

            alt="image"
            onError={(e) => {
              e.currentTarget.src = defaultImage;
            }}
          />
          <p>{image.description}</p>
          <div className="flex flex-row gap-2 items-center">
          <Button
            onClick={() => window.open('https://www.amazon.com/', '_blank')}
            variant="outline"
            >
            buy it
          </Button>
          <p>Subtennatility Score: {image.subtennatilityScore} / 100</p>
          </div>
        </div>
      ))}
    </div>
  );
};

import { useInputStore } from '@/libs/zustand/input';
import { useDebugStore } from '@/libs/zustand/debug';
import Image from 'next/image';
import { Button } from '@/components/ui/button';

export const Debug = () => {
  const { images } = useInputStore();
  const { isDebugOpen, triggerDebugOpen } = useDebugStore();

  if (!isDebugOpen) {
    return null;
  }

  return (
    <div className="fixed top-0 right-0 z-50 bg-gray-100 p-4 h-full w-sm">
      <Button variant="outline" onClick={triggerDebugOpen}>
        X
      </Button>
      <div className="flex flex-col items-center justify-center  transform -scale-x-100">
        {images.map((image, idx) => (
          <Image
            key={idx}
            src={`data:image/png;base64,${image}`}
            width={320}
            height={180}
            alt="image"
          />
        ))}
      </div>
    </div>
  );
};

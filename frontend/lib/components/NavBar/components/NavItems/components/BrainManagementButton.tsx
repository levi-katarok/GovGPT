import Link from "next/link";
import { BsFillCollectionFill } from "react-icons/bs";
import { MdSettings } from "react-icons/md";

export const BrainManagementButton = (): JSX.Element => {
  return (
    <Link href={"/brains-management"}>
      <button type="button" className="flex items-center focus:outline-none">
        <MdSettings className="w-6 h-6" color="gray" />
        <BsFillCollectionFill className="w-3 h-3" color="gray" />
      </button>
    </Link>
  );
};

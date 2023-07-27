import Image from "next/image";
import Link from "next/link";

export const Logo = (): JSX.Element => {
  return (
    <Link href={"/"} className="flex items-center gap-4">
      <Image
        className="rounded-full"
        src={"/Full Logo - Light Name.png"}
        alt="Quivr Logo"
        width={100}
        height={100}
      />
      {/* <h1 className="font-bold">GovGPT</h1> */}
    </Link>
  );
};

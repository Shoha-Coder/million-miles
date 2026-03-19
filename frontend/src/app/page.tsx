import { redirect } from "next/navigation";

// Root path always goes to the car listing
export default function RootPage() {
  redirect("/cars");
}

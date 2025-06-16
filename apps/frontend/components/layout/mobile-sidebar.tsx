"use client";

import { Menu } from "lucide-react";

import { Sidebar } from "./sidebar";

import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

export function MobileSidebar() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button className="md:hidden" size="icon" variant="ghost">
          <Menu className="h-5 w-5" />
          <span className="sr-only">Toggle sidebar</span>
        </Button>
      </SheetTrigger>
      <SheetContent className="p-0 w-64" side="left">
        <Sidebar />
      </SheetContent>
    </Sheet>
  );
}

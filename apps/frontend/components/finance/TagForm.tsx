"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Tag } from "@/types";

const tagSchema = z.object({
  name: z
    .string()
    .min(1, "Tag name is required")
    .max(50, "Tag name too long")
    .regex(
      /^[a-zA-Z0-9\s-_]+$/,
      "Tag name can only contain letters, numbers, spaces, hyphens, and underscores",
    ),
});

type TagFormData = z.infer<typeof tagSchema>;

interface TagFormProps {
  tag?: Tag | null;
  onSubmit: (data: TagFormData) => Promise<void>;
  onCancel: () => void;
}

export function TagForm({ tag, onSubmit, onCancel }: TagFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<TagFormData>({
    resolver: zodResolver(tagSchema),
    defaultValues: {
      name: tag?.name || "",
    },
  });

  const handleSubmit = async (data: TagFormData) => {
    try {
      setIsSubmitting(true);
      await onSubmit(data);
      form.reset();
    } catch (error) {
      console.error("Failed to submit tag:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const watchedName = form.watch("name");
  const previewTag = watchedName.trim();

  return (
    <Form {...form}>
      <form className="space-y-6" onSubmit={form.handleSubmit(handleSubmit)}>
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tag Name</FormLabel>
              <FormControl>
                <Input
                  placeholder="Enter tag name (e.g., travel, food, work)"
                  {...field}
                />
              </FormControl>
              <FormMessage />
              {previewTag && (
                <div className="text-sm text-muted-foreground">
                  Preview:{" "}
                  <span className="inline-flex items-center px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                    #{previewTag}
                  </span>
                </div>
              )}
            </FormItem>
          )}
        />

        <div className="space-y-3">
          <h4 className="text-sm font-medium">Tag Guidelines</h4>
          <ul className="text-sm text-muted-foreground space-y-1">
            <li>• Keep tags short and descriptive</li>
            <li>• Use lowercase for consistency</li>
            <li>• Common examples: food, transport, entertainment, bills</li>
            <li>• Avoid special characters except hyphens and underscores</li>
          </ul>
        </div>

        <div className="flex gap-3 pt-4">
          <Button
            disabled={isSubmitting}
            type="button"
            variant="outline"
            onClick={onCancel}
          >
            Cancel
          </Button>
          <Button disabled={isSubmitting || !previewTag} type="submit">
            {isSubmitting ? "Saving..." : tag ? "Update Tag" : "Create Tag"}
          </Button>
        </div>
      </form>
    </Form>
  );
}

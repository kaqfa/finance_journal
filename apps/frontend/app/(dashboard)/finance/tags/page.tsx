"use client";

import { useState, useEffect } from "react";
import { Plus, Edit, Trash2, Tag as TagIcon, Hash } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import financeAPI from "@/lib/api/finance";
import { Tag } from "@/types";
import { TagForm } from "@/components/finance/TagForm";

export default function TagsPage() {
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingTag, setEditingTag] = useState<Tag | null>(null);
  const [searchTerm, setSearchTerm] = useState("");

  const fetchTags = async () => {
    try {
      setLoading(true);
      const response = await financeAPI.getTags();

      setTags(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error("Failed to fetch tags:", error);
      setTags([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTags();
  }, []);

  const handleCreateTag = async (data: any) => {
    try {
      await financeAPI.createTag(data);
      fetchTags();
      setDialogOpen(false);
    } catch (error) {
      console.error("Failed to create tag:", error);
    }
  };

  const handleEditTag = (tag: Tag) => {
    setEditingTag(tag);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingTag(null);
  };

  const filteredTags = tags.filter((tag) =>
    tag.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Tags</h1>
        </div>
        <Card className="animate-pulse">
          <CardHeader>
            <div className="h-6 bg-gray-200 rounded w-1/3" />
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="h-10 bg-gray-100 rounded" />
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Tags</h1>
          <p className="text-muted-foreground">
            Label your transactions for better organization and filtering
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Tag
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>
                {editingTag ? "Edit Tag" : "Create Tag"}
              </DialogTitle>
            </DialogHeader>
            <TagForm
              tag={editingTag}
              onCancel={handleCloseDialog}
              onSubmit={handleCreateTag}
            />
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Hash className="h-5 w-5 text-blue-600" />
              All Tags
              <Badge variant="secondary">{filteredTags.length}</Badge>
            </CardTitle>
            <div className="w-72">
              <Input
                className="w-full"
                placeholder="Search tags..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {filteredTags.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              <TagIcon className="h-16 w-16 mx-auto mb-4 opacity-50" />
              {searchTerm ? (
                <>
                  <p className="text-lg font-medium">No tags found</p>
                  <p>Try adjusting your search terms</p>
                </>
              ) : (
                <>
                  <p className="text-lg font-medium">No tags yet</p>
                  <p>Create your first tag to start organizing transactions</p>
                </>
              )}
            </div>
          ) : (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {filteredTags.map((tag) => (
                <div
                  key={tag.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent transition-colors group"
                >
                  <div className="flex items-center gap-3 min-w-0 flex-1">
                    <div className="p-2 rounded-lg bg-blue-100 text-blue-600 flex-shrink-0">
                      <Hash className="h-4 w-4" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="font-medium truncate">{tag.name}</p>
                      <p className="text-sm text-muted-foreground">
                        Created {new Date(tag.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        className="opacity-0 group-hover:opacity-100 transition-opacity"
                        size="sm"
                        variant="ghost"
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => handleEditTag(tag)}>
                        <Edit className="mr-2 h-4 w-4" />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Tag Usage Statistics */}
      {tags.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Tag Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {tags.length}
                </div>
                <div className="text-sm text-muted-foreground">Total Tags</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {
                    tags.filter(
                      (tag) =>
                        new Date(tag.created_at) >
                        new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
                    ).length
                  }
                </div>
                <div className="text-sm text-muted-foreground">
                  Created This Week
                </div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {
                    tags.filter(
                      (tag) =>
                        new Date(tag.created_at) >
                        new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
                    ).length
                  }
                </div>
                <div className="text-sm text-muted-foreground">
                  Created This Month
                </div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-orange-600">0</div>
                <div className="text-sm text-muted-foreground">Most Used</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

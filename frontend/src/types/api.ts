export type UserRole =
  | "student"
  | "teacher"
  | "mentor"
  | "school_manager"
  | "org_manager"
  | "content_editor"
  | "moderator"
  | "admin";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  city?: string;
  state?: string;
  country?: string;
  interests: string[];
  robotics_programs: string[];
}

export interface Course {
  id: number;
  public_id: string;
  title: string;
  slug: string;
  description: string;
  level: "beginner" | "intermediate" | "advanced";
  workload_hours: number;
  is_free: boolean;
  status: string;
  progress_percent?: string;
  modules?: CourseModule[];
}

export interface CourseModule {
  id: number;
  title: string;
  description: string;
  order: number;
  lessons: Lesson[];
}

export interface Lesson {
  id: number;
  title: string;
  lesson_type: string;
  duration_minutes: number;
  order: number;
}

export interface Team {
  id: number;
  name: string;
  team_number: string;
  program: string;
  season_year: number;
  status: string;
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

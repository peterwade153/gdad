/**
 * Represents a payload for the Person.
 */
export interface PersonPayload {
    id: number;
    name: string;
    surname: string;
    identity_number: string;
    generation: number;
    birth_date: string | null;
    father_id: string | null;
    mother_id: string | null;
}

export interface Payload { 
    people: PersonPayload[],
    generations: number
}

export interface RootAscendantPayload {
    root_ascendants: PersonPayload[],
    max_depth_reached: number
}

export interface TreePlaceholderProps {
    icon: string;
    iconBgColor: string;
    iconTextColor: string;
    title: string;
    description: React.ReactNode;
}

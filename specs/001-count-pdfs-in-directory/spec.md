# Feature Specification: Count documents in a directory

**Feature Branch**: `001-count-pdfs-in-directory`  
**Created**: 2025-03-27  
**Status**: Draft  
**Input**: User description: "I want to create a simple command line application that given a directory will count the number of PDF and DOC files in it."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get document count for a folder (Priority: P1)

A user wants to point a small command-line tool at a folder on their computer and learn how many
PDF or DOC documents sit **directly** in that folder (not inside subfolders), so they can verify
collections, audit folders, or prepare batches without manually counting.

**Why this priority**: This is the entire product outcome; delivering it alone is a usable tool.

**Independent Test**: Create a disposable folder with a known mix of files (including PDFs, DOCs,
and unrelated files, varied name casing, optional subfolder with extra matching files). Run the tool
against that folder and verify the count matches only the in-scope files that are immediate children
of that folder, and that
behavior matches **Edge Cases** below for invalid inputs.

**Acceptance Scenarios**:

1. **Given** a directory that contains files whose names end in `.pdf` or `.doc` (any letter casing)
   plus unrelated files, **When** the user runs the tool with that directory, **Then** the user sees
   the total count of matching files.
2. **Given** an empty directory, **When** the user runs the tool with that directory, **Then** the
   user sees a count of zero.
3. **Given** a directory that has a subfolder containing additional matching files, **When** the user
   runs the tool with the parent directory, **Then** files inside the subfolder are not included in
   the count.
4. **Given** a path that does not exist or is not a directory (for example a file path), **When** the
   user runs the tool with that path, **Then** the user sees a clear, human-readable message
   explaining the problem and the outcome is distinguishable from success (no silent success).
5. **Given** a directory that cannot be read (for example permission denied), **When** the user runs
   the tool with that path, **Then** the user sees a clear failure indication and does not receive a
   misleading document count.
6. **Given** a directory containing an entry whose name ends with `.pdf` or `.doc` but which is not a regular
   file (for example a subfolder named `archive.pdf`), **When** the user runs the tool, **Then** that
   entry is not included in the document count.
7. **Given** a directory that includes regular files named like `.report.pdf` or `.report.doc` (leading dot), **When**
   the user runs the tool, **Then** that file is included in the count.
8. **Given** a directory path that contains spaces or non-ASCII characters and that the user’s
   environment allows passing that path to the tool, **When** the user runs the tool, **Then** the
   count matches the number of in-scope files in that directory.

### Edge Cases

- The supplied path does not exist.
- The supplied path exists but is not a directory (e.g., it is a regular file).
- The process lacks permission to read the directory or some entries in it.
- The directory contains no matching files, only matching files, or a mix including hidden names
  (e.g., `.report.pdf`, `.report.doc`).
- File names use different casing for the extension (`.pdf`, `.PDF`, `.Pdf`, `.doc`, `.DOC`, `.Doc`).
- Names look like matching files but are not regular files (e.g., directories or special entries)—
  the tool MUST NOT treat those as in-scope files for counting.
- Paths contain spaces or non-ASCII characters (must still be supportable if the environment allows
  the user to select that path).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The tool MUST accept a single directory path as its primary input (as provided by the
  user in the command-line environment).
- **FR-002**: The tool MUST count only entries in that directory that are in-scope documents for this
  feature: regular files whose name ends with `.pdf` or `.doc` in a case-insensitive way.
- **FR-003**: The tool MUST NOT include in-scope files (or any files) located only inside descendant
  subfolders—only immediate children of the given directory are considered.
- **FR-004**: On success, the tool MUST present the count to the user in an unambiguous way (a single
  numeric result for the document total).
- **FR-005**: On failure (missing path, wrong type, unreadable directory), the tool MUST surface a
  clear explanation to the user and MUST NOT report a successful count as if the directory were valid.

### Key Entities

- **Target directory**: The folder the user specifies; the scope of scanning is only its immediate
  children.
- **In-scope document file**: A regular file in that directory whose filename has a case-insensitive
  `.pdf` or `.doc` suffix.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For any prepared directory where the correct number of in-scope files is known by
  independent means (manual labeling), the value the user obtains is exactly that number.
- **SC-002**: For a directory containing up to one thousand immediate child entries (files and
  folders combined), the user receives the numeric result within five seconds on a typical personal
  computer under normal interactive use.
- **SC-003**: In failure scenarios defined in **FR-005**, one hundred percent of exercise runs must
  produce a clear error indication (message or non-success outcome), never a misleading document count.

## Assumptions

- “Simple” scope means **one** directory argument and **non-recursive** counting unless a future
  feature changes that; subfolders are ignored for counting.
- Detection is **by filename extension only** (`.pdf` and `.doc`, case-insensitive), not by
  inspecting file contents.
- The tool is used interactively by a person who can read short text output; no graphical interface
  is required.
- Locale and path rules follow what the user’s operating environment normally allows when passing a
  path to a command-line program.

## Constitution Alignment *(mandatory)*

Per `.specify/memory/constitution.md`:

- **Testing**: **Independent Test** above exercises the primary path, empty folder, subfolder
  exclusion, and invalid-path behavior; acceptance scenarios map to each **Edge Cases** item that
  defines user-visible behavior.
- **UX consistency**: First CLI behavior for this repo—success shows one numeric result; failures use
  clear language suitable for a non-technical operator reading the terminal.
- **Performance**: **SC-002** states an interactive-response budget for a bounded folder size.

Functional requirements above MUST trace to stories and success criteria; non-functional expectations
MUST not live only in informal prose.

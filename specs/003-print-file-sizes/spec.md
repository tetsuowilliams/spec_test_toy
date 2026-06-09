# Feature Specification: Print file sizes in a directory

**Feature Branch**: `003-print-file-sizes`  
**Created**: 2026-06-09  
**Status**: Draft  
**Input**: User description: "I want to be able to print the size of files in a certain directory"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - List file sizes for a folder (Priority: P1)

A user wants to point the existing command-line tool at a folder and see the size of each regular
file that sits **directly** in that folder (not inside subfolders), so they can audit disk usage,
compare file weights, or prepare transfers without opening each file manually.

**Why this priority**: This is the entire product outcome; delivering it alone is a usable tool.

**Independent Test**: Create a disposable folder with a known mix of regular files (varied sizes,
including a zero-byte file), subfolders containing additional files, and unrelated entry types
(for example a subdirectory or special entry). Run the tool against that folder and verify each
listed line matches the expected file name and byte size for immediate children only, and that
behavior matches **Edge Cases** below for invalid inputs.

**Acceptance Scenarios**:

1. **Given** a directory that contains several regular files with known byte sizes, **When** the user
   runs the tool in file-size listing mode with that directory, **Then** the user sees one line per
   in-scope file showing that file’s name and its size in bytes.
2. **Given** an empty directory, **When** the user runs the tool in file-size listing mode, **Then**
   the user sees no file-size lines (successful outcome with no listed files).
3. **Given** a directory that has a subfolder containing additional regular files, **When** the user
   runs the tool with the parent directory, **Then** files inside the subfolder are not included in
   the listing.
4. **Given** a path that does not exist or is not a directory (for example a file path), **When** the
   user runs the tool with that path, **Then** the user sees a clear, human-readable message
   explaining the problem and the outcome is distinguishable from success (no silent success).
5. **Given** a directory that cannot be read (for example permission denied), **When** the user runs
   the tool with that path, **Then** the user sees a clear failure indication and does not receive
   a misleading file listing.
6. **Given** a directory containing entries that are not regular files (for example subfolders or
   symbolic links to files), **When** the user runs the tool, **Then** those entries are not listed
   as files with sizes.
7. **Given** a directory that includes regular files with leading-dot names (for example
   `.hidden.txt`), **When** the user runs the tool, **Then** those files are included in the listing
   with their sizes.
8. **Given** a directory path that contains spaces or non-ASCII characters and that the user’s
   environment allows passing that path to the tool, **When** the user runs the tool, **Then** the
   listing matches the in-scope files and sizes in that directory.
9. **Given** a directory containing a zero-byte regular file, **When** the user runs the tool,
   **Then** that file appears in the listing with a size of zero bytes.

### Edge Cases

- The supplied path does not exist.
- The supplied path exists but is not a directory (e.g., it is a regular file).
- The process lacks permission to read the directory or to stat some entries in it.
- The directory contains no regular files, only regular files, or a mix including hidden names
  (e.g., `.config`).
- Entries look like files but are not regular files (e.g., directories, symbolic links)—the tool MUST
  NOT list those as sized files.
- Paths contain spaces or non-ASCII characters (must still be supportable if the environment allows
  the user to select that path).
- A regular file’s reported size is zero bytes.
- Multiple files share the same size; each MUST still appear as its own line with the correct name.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The tool MUST accept a single directory path as its primary input (as provided by the
  user in the command-line environment) when operating in file-size listing mode.
- **FR-002**: The tool MUST list only immediate-child entries in that directory that are regular
  files, each with its filesystem-reported size in bytes.
- **FR-003**: The tool MUST NOT include regular files (or any files) located only inside descendant
  subfolders—only immediate children of the given directory are considered.
- **FR-004**: On success, the tool MUST present one line per in-scope file so the user can
  unambiguously match each file name to its byte size; lines MUST be ordered alphabetically by file
  name (case-sensitive byte order as displayed to the user).
- **FR-005**: On failure (missing path, wrong type, unreadable directory), the tool MUST surface a
  clear explanation to the user and MUST NOT report a successful listing as if the directory were
  valid.
- **FR-006**: The tool MUST NOT follow symbolic links when deciding whether an entry is a regular
  file or when reading its size; a symbolic link entry MUST NOT appear as a listed file even if its
  target is a regular file.

### Key Entities

- **Target directory**: The folder the user specifies; the scope of scanning is only its immediate
  children.
- **Listed file**: A regular file in that directory with a filesystem-reported byte size and a
  display name identifying that file within the listing.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For any prepared directory where the correct set of immediate-child regular files and
  byte sizes is known by independent means (manual measurement), every line the user obtains matches
  that set exactly (same names and sizes, no omissions, no extras).
- **SC-002**: For a directory containing up to one thousand immediate child entries (files and
  folders combined), the user receives the complete listing within five seconds on a typical personal
  computer under normal interactive use.
- **SC-003**: In failure scenarios defined in **FR-005**, one hundred percent of exercise runs must
  produce a clear error indication (message or non-success outcome), never a misleading file listing.

## Assumptions

- File-size listing is a **new mode** of the existing command-line tool, invoked explicitly by the
  user (for example a dedicated flag), so default document-count behavior remains unchanged.
- Scope is **non-recursive**: only immediate children of the given directory are listed, consistent
  with the tool’s existing directory-scanning behavior.
- **All** regular files in the directory are in scope; there is no extension or type filter.
- Sizes are reported in **bytes** as the filesystem reports for each regular file (logical content
  length), not human-readable units, so results are exact and easy to verify.
- The tool is used interactively by a person who can read short text output; no graphical interface
  is required.
- Locale and path rules follow what the user’s operating environment normally allows when passing a
  path to a command-line program.

## Constitution Alignment *(mandatory)*

Per `.specify/memory/constitution.md`:

- **Testing**: **Independent Test** above exercises the primary path, empty folder, subfolder
  exclusion, zero-byte files, and invalid-path behavior; acceptance scenarios map to each **Edge
  Cases** item that defines user-visible behavior.
- **UX consistency**: Reuse the existing tool’s CLI patterns—clear stderr errors and non-zero exit on
  failure; success output on stdout only. File-size listing is intentionally multi-line (unlike the
  single-number count modes) and MUST be documented as that deviation.
- **Performance**: **SC-002** states an interactive-response budget for a bounded folder size.

Functional requirements above MUST trace to stories and success criteria; non-functional expectations
MUST not live only in informal prose.

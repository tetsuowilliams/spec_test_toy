# Feature Specification: Count directories that contain PDFs

**Feature Branch**: `002-count-pdf-directories`  
**Created**: 2026-03-27  
**Status**: Draft  
**Input**: User description: "I want to be able to count the directories that contain PDFs."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Count PDF-holding directories under a folder (Priority: P1)

A user wants to point a command-line tool at a folder and learn **how many directories** under that
tree (including the starting folder when applicable) **directly contain at least one PDF file**, so
they can see how many “PDF-bearing” folders exist without opening each one by hand.

**Why this priority**: This is the full outcome of the feature; delivering it alone is a complete,
usable capability.

**Independent Test**: Create a disposable directory tree with a known layout: some folders with PDFs
directly inside, some folders whose only PDFs sit in deeper descendants, nested chains, empty folders,
and non-PDF files. Run the tool on the tree root and verify the numeric total equals the number of
directories that have at least one qualifying PDF among their **immediate children only**. Verify
failure behavior for invalid paths matches the **Edge Cases** list.

**Acceptance Scenarios**:

1. **Given** a root directory whose immediate children include two subfolders; the first subfolder
   contains `a.pdf` and the second contains only `notes.txt`, **When** the user runs the tool on the
   root, **Then** the count is one (only the first subfolder qualifies; the root has no direct PDF).
2. **Given** a root directory that itself contains `report.pdf` and also contains an empty
   subfolder, **When** the user runs the tool on the root, **Then** the count is one (the root
   qualifies).
3. **Given** a chain `root/sub/deep/` where the only PDF is at `root/sub/deep/file.pdf`, **When** the
   user runs the tool on `root`, **Then** the count is one (only `deep` has a direct PDF child).
4. **Given** a directory tree with no PDF files anywhere, **When** the user runs the tool, **Then** the
   count is zero.
   
5. **Given** a directory where two different immediate subfolders each contain at least one PDF,
   **When** the user runs the tool on the parent, **Then** the count includes both subfolders (and
   any other qualifying directories elsewhere in the tree under that parent).
6. **Given** a folder that contains one subfolder, and that subfolder holds multiple PDF files,
   **When** the user runs the tool, **Then** that subfolder contributes **one** toward the count, not
   one per file.
7. **Given** file names using different casing for the extension (`.pdf`, `.PDF`, `.Pdf`) on regular
   files, **When** the user runs the tool, **Then** each such regular file counts toward its parent
   directory’s “contains PDF” status consistent with the rules below.
8. **Given** an entry whose name ends with `.pdf` but is **not** a regular file (for example a
   subfolder named `archive.pdf`), **When** the user runs the tool, **Then** that entry does **not**
   cause its parent directory to qualify as containing a PDF.
9. **Given** a regular file named like `.report.pdf` (leading dot) in a directory, **When** the user
   runs the tool, **Then** that file can qualify its parent directory the same as any other in-scope
   PDF file name.
10. **Given** a path that does not exist or is not a directory, **When** the user runs the tool,
    **Then** the user sees a clear, human-readable explanation and the outcome is distinguishable from
    success.
11. **Given** a directory that cannot be fully traversed (for example permission denied on a
    subfolder), **When** the user runs the tool, **Then** the user sees a clear failure indication and
    does not receive a misleading count.
12. **Given** a directory path that contains spaces or non-ASCII characters and the user’s
    environment allows passing that path to the tool, **When** the user runs the tool, **Then** the
    count matches the number of qualifying directories in that tree.

### Edge Cases

- The supplied path does not exist.
- The supplied path exists but is not a directory (for example it is a regular file).
- Some part of the tree cannot be read (permissions, transient errors).
- The tree is large or deeply nested; the user still expects a timely result under normal interactive
  use (see success criteria).
- No directory in the tree directly contains a PDF; result must be zero.
- Multiple PDFs in the same directory must not inflate the directory count.
- Names look like PDFs but are not regular files—must not qualify the parent directory.
- Paths contain spaces or non-ASCII characters when the environment supports supplying them.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The tool MUST accept a single directory path as its primary input (as provided by the
  user in the command-line environment).
- **FR-002**: The tool MUST consider the entire directory **tree** rooted at that path: every
  directory reachable from the root through nested subfolders is evaluated.
- **FR-003**: A directory counts toward the total if and only if it has **at least one immediate
  child** that is an in-scope PDF: a **regular file** whose name ends with `.pdf` in a
  case-insensitive way. PDFs that appear only inside descendant subfolders (not as immediate
  children of the directory being evaluated) do not make that ancestor directory count.
- **FR-004**: Each qualifying directory MUST contribute exactly **one** to the total, regardless of
  how many in-scope PDF files sit directly inside it.
- **FR-005**: On success, the tool MUST present the total count to the user in an unambiguous way (a
  single numeric result for the number of qualifying directories).
- **FR-006**: On failure (missing path, wrong type, unreadable tree as specified in edge cases), the
  tool MUST surface a clear explanation to the user and MUST NOT report a successful directory count
  as if the input were fully valid and traversable.

### Key Entities

- **Root directory**: The folder the user specifies; traversal starts here and includes all
  descendant directories unless traversal fails.
- **PDF file (in scope)**: A regular file whose filename has a case-insensitive `.pdf` suffix;
  detection is by name only, not by file content.
- **Qualifying directory**: A visited directory that has at least one in-scope PDF among its immediate
  children.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For any prepared directory tree where the correct number of qualifying directories is
  known by independent means (manual labeling), the value the user obtains is exactly that number.
- **SC-002**: For a tree containing up to two thousand directories total and up to ten thousand files
  total, the user receives the numeric result within ten seconds on a typical personal computer under
  normal interactive use.
- **SC-003**: In failure scenarios defined in **FR-006**, one hundred percent of exercise runs must
  produce a clear error indication (message or non-success outcome), never a misleading directory
  count.

## Assumptions

- PDF detection is **by filename extension only** (`.pdf`, case-insensitive), not by inspecting file
  contents—consistent with the existing “count PDFs in a directory” behavior in this project.
- “Contain PDFs” means **directly contain** at least one qualifying PDF file as an immediate child; the
  tool **does** recurse **into** subfolders to visit every directory and apply that rule at each level.
- Symbolic links and other special file types are treated according to what the user’s operating
  environment normally does when traversing directories (the spec does not require special follow/skip
  rules beyond clear failure when traversal cannot continue).
- The tool is used interactively by a person who can read short text output; no graphical interface is
  required.
- Locale and path rules follow what the user’s operating environment normally allows when passing a
  path to a command-line program.

## Constitution Alignment *(mandatory)*

Per `.specify/memory/constitution.md`:

- **Testing**: The **Independent Test** and acceptance scenarios cover the primary path, multi-level
  trees, per-directory deduplication, extension and file-type rules, empty trees, and invalid or
  partially unreadable inputs aligned with **Edge Cases**.
- **UX consistency**: Delivers a single numeric result on success and clear, human-readable failures,
  matching the established CLI pattern in this repository.
- **Performance**: **SC-002** states an interactive-response budget for a bounded tree size.

Functional requirements above MUST trace to stories and success criteria; non-functional expectations
MUST not live only in informal prose.

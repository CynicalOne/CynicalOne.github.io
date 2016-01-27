import os
import markdown
import codecs

spells_directory = "./docs/spellcasting/spells"
output_directory = "./docs/spellcasting/spell_indexes"
spells_relative_link = "/spellcasting/spells"

def generate_formatted_title(title):
    if len(title) == 1 and title.isdigit():
        if title == "0":
            return "## Cantrips (0 level)"
        if title == "1":
            return "## 1st Level"
        if title == "2":
            return "## 2nd level"
        if title == "3":
            return "## 3rd level"
        else:
            return "## %sth level" % title
    else:
        return "## %s" % title.capitalize()

def convert_to_linkable_spell_name(spell):
    return spell.replace(" ", "_").replace("'", "").replace("/", "").lower()

def create_output_directory():
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

def output_file(sorted_spells, filename, page_title):
    output = []
    output.append(page_title)
    for category in sorted(sorted_spells):
        # Insert the header
        output.append(generate_formatted_title(category))
        for spell in sorted_spells[category]:
            spell_link_name = convert_to_linkable_spell_name(spell)
            output.append("[%s](%s/%s)   " % (spell, spells_relative_link, spell_link_name))
        output.append(" ")
    with open("%s/%s" % (output_directory, filename), "w") as f:
        for line in output:
            f.write(line + "\n")

if __name__ == "__main__":
    create_output_directory()
    spell_files = os.listdir(spells_directory)
    spells_by_level = {}
    spells_by_school = {}
    spells_by_name = {}
    for filename in spell_files:
        md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
        input_file = codecs.open("%s/%s" % (spells_directory, filename), mode="r",
                                 encoding="utf-8")
        md.convert(input_file.read())
        level = md.Meta["level"][0]
        name = md.Meta["name"][0]
        school = md.Meta["school"][0]
        name_category = md.Meta["name"][0][0].capitalize()
        # Append spell to spells_by_level
        if level in spells_by_level:
            spells_by_level[level].append(name)
        else:
            spells_by_level[level] = [name]

        # Append spell to spells_by_school
        if school in spells_by_school:
            spells_by_school[school].append(name)
        else:
            spells_by_school[school] = [name]

        # Append spell to spells_by_name
        if name_category in spells_by_name:
            spells_by_name[name_category].append(name)
        else:
            spells_by_name[name_category] = [name]
    output_file(spells_by_level, "spells_by_level.md", "# Spells by Level")
    output_file(spells_by_school, "spells_by_school.md", "# Spells by School")
    output_file(spells_by_name, "spells_by_name.md", "# Spells by Name")
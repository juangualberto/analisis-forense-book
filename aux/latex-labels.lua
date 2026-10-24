local replacements = {
  ["á"] = "a",
  ["é"] = "e",
  ["í"] = "i",
  ["ó"] = "o",
  ["ú"] = "u",
  ["ü"] = "u",
  ["ñ"] = "n",
  ["Á"] = "A",
  ["É"] = "E",
  ["Í"] = "I",
  ["Ó"] = "O",
  ["Ú"] = "U",
  ["Ü"] = "U",
  ["Ñ"] = "N"
}

local function ascii_id(id)
  for unicode, ascii in pairs(replacements) do
    id = id:gsub(unicode, ascii)
  end

  id = id:lower()

  id = id:gsub("[^%w%-_%.:]", "-")
  id = id:gsub("%-+", "-")
  id = id:gsub("^%-+", "")
  id = id:gsub("%-+$", "")

  return id
end

function Header(el)
  if el.identifier and el.identifier ~= "" then
    el.identifier = ascii_id(el.identifier)
  end

  return el
end
